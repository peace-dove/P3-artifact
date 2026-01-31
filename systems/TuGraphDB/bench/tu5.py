from neo4j import GraphDatabase
import csv
import time
from collections import defaultdict

# Configuration
URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")
DATABASE_NAME = "tugraph_sf10"
PARAM_FILE = "/data/dataset/sf10/params/complex_5_param.csv"

BATCH_SIZE = 100
REPETITIONS_PER_BATCH = 10

all_query_execution_times = []
all_query_results_counts = []

def execute_single_query(session, query, param_id):
    start_time_sec = time.time()
    try:
        result = session.run(query)
        records = result.data()
        elapsed = time.time() - start_time_sec
        return elapsed, len(records)
    except Exception as e:
        elapsed = time.time() - start_time_sec
        return elapsed, -1

def read_params_and_benchmark():
    global all_query_execution_times, all_query_results_counts

    print(f"Connected to {URI}, database: {DATABASE_NAME}")

    current_batch_params = []
    param_counter = 0

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with open(PARAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                param_counter += 1
                current_batch_params.append({
                    "node_id": row["id"].strip(),
                    "start_time": int(row["startTime"]),
                    "end_time": int(row["endTime"]),
                    "original_row_num": param_counter
                })

                if len(current_batch_params) == BATCH_SIZE:
                    process_batch(driver, current_batch_params, param_counter - BATCH_SIZE + 1)
                    current_batch_params = []

            if current_batch_params:
                process_batch(driver, current_batch_params, param_counter - len(current_batch_params) + 1)

    if all_query_execution_times:
        total_time = sum(all_query_execution_times)
        avg_time = total_time / len(all_query_execution_times)
        min_time = min(all_query_execution_times)
        max_time = max(all_query_execution_times)
        total_queries_executed = len(all_query_execution_times)
        total_results_count = sum(c for c in all_query_results_counts if c != -1)

        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        print(f"URI:                     {URI}")
        print(f"Database:                {DATABASE_NAME}")
        print(f"Batch size:              {BATCH_SIZE}")
        print(f"Repetitions per batch:   {REPETITIONS_PER_BATCH}")
        print(f"Total queries:           {total_queries_executed}")
        print(f"Total time:              {total_time:.4f} s")
        print(f"Average time:            {avg_time:.4f} s")
        print(f"Min time:                {min_time:.4f} s")
        print(f"Max time:                {max_time:.4f} s")
        print(f"Total results:           {total_results_count}")
        print("=" * 60)
    else:
        print("No queries executed successfully.")

def process_batch(driver, batch_params, start_param_num):
    print(f"\n{'#'*10} Processing batch: {start_param_num} - {start_param_num + len(batch_params) - 1} {'#'*10}")

    batch_repetition_times = defaultdict(list)
    batch_repetition_results = defaultdict(list)

    with driver.session(database=DATABASE_NAME) as session:
        for repetition in range(REPETITIONS_PER_BATCH):
            print(f"  --- Repetition {repetition + 1}/{REPETITIONS_PER_BATCH} ---")
            for param_idx, param in enumerate(batch_params):
                query = f"""
MATCH (person:Person {{id:{param['node_id']}}})-[e1:own]->(src:Account)
WITH src
MATCH p=(src)-[e2:transfer*1..3]->(dst:Account)
WHERE isAsc(getMemberProp(e2, 'timestamp'))=true AND
      head(getMemberProp(e2, 'timestamp')) > {param['start_time']} AND
      last(getMemberProp(e2, 'timestamp')) < {param['end_time']}
WITH DISTINCT getMemberProp(nodes(p), 'id') as path, length(p) as len
ORDER BY len DESC
WHERE hasDuplicates(path)=false
RETURN path;
"""
                elapsed, num_results = execute_single_query(session, query, param['node_id'])
                
                batch_repetition_times[param['original_row_num']].append(elapsed)
                batch_repetition_results[param['original_row_num']].append(num_results)
                
                all_query_execution_times.append(elapsed)
                all_query_results_counts.append(num_results)

    print(f"\n  --- Batch {start_param_num}-{start_param_num + len(batch_params) - 1} Statistics ---")
    for original_row_num, times in batch_repetition_times.items():
        avg_t = sum(times) / len(times)
        min_t = min(times)
        max_t = max(times)
        print(f"    Row {original_row_num} (ID: {batch_params[original_row_num-start_param_num]['node_id']}): "
              f"Avg {avg_t:.4f}s (Min: {min_t:.4f}s, Max: {max_t:.4f}s)")

if __name__ == "__main__":
    print("Starting benchmark...")
    try:
        read_params_and_benchmark()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
