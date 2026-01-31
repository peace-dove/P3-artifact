from neo4j import GraphDatabase
import csv
import time

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
# PARAM_FILE = "params_sf100/complex_5_param.csv"
PARAM_FILE = "params_sf10/complex_5_param.csv"

BATCH_SIZE = 100

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

execution_times = []
results_count = 0

def execute_query(tx, query):
    result = tx.run(query)
    return result.data()

def read_params_and_execute():
    global results_count

    success_count = 0
    failure_count = 0

    with open(PARAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        
        for i, row in enumerate(reader, start=1):
            try:
                node_id = row["id"].strip()
                start_time = int(row["startTime"])   # long in Python
                end_time = int(row["endTime"])       # long in Python
            except Exception as e:
                execution_times.append(0.0)
                failure_count += 1
                continue

            query = f"""
MATCH
  (person:Person {{personId: '{node_id}'}})-[edge1:PERSON_OWN_ACCOUNT]->(src:Account),
  p=(src)-[edge2:ACCOUNT_TRANSFER_ACCOUNT*1..3]->(dst:Account) 
WITH p, [e IN relationships(p) | e.createTime] AS ts, [n IN nodes(p) | n.personid ] AS nid
WHERE reduce(curr = head(ts), x IN tail(ts) | CASE WHEN curr < x THEN x ELSE 9223372036854775807 end) <> 9223372036854775807 
  AND all(e IN edge2 WHERE {start_time} < e.createTime < {end_time}) 
RETURN p AS path
ORDER BY length(p) DESC;
"""
            start_time_sec = time.time()

            try:
                with driver.session() as session:
                    records = session.read_transaction(execute_query, query)

                elapsed = time.time() - start_time_sec
                execution_times.append(elapsed)
                results_count += len(records)
                success_count += 1
                print(f"✅ Success | Time: {elapsed:.4f}s | Results: {len(records)} rows")
                input()


            except Exception as e:
                elapsed = time.time() - start_time_sec
                execution_times.append(elapsed)
                failure_count += 1

            if i % BATCH_SIZE == 0:
                avg_so_far = sum(execution_times) / len(execution_times)
                print(f"📊 Processed {i} rows | "
                      f"Success: {success_count} Failure: {failure_count} | "
                      f"Average Time: {avg_so_far:.4f}s | "
                      f"Cumulative Results: {results_count}")

    # Final statistics
    if execution_times:
        total_time = sum(execution_times)
        avg_time = total_time / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        total_queries = len(execution_times)

        print("\n" + "="*60)
        print("📈 Query Execution Completed (Final Statistics)")
        print("="*60)
        print(f"Total Rows Processed:      {success_count + failure_count}")
        print(f"Successful Executions:     {success_count}")
        print(f"Failed Executions:         {failure_count}")
        print(f"Total Execution Time:      {total_time:.4f} seconds")
        print(f"Average Time per Query:    {avg_time:.4f} seconds")
        print(f"Minimum Time per Query:    {min_time:.4f} seconds")
        print(f"Maximum Time per Query:    {max_time:.4f} seconds")
        print(f"Cumulative Results Returned: {results_count} rows")
        print("="*60)
    else:
        print("⚠️ No successful queries executed.")

if __name__ == "__main__":
    try:
        start_total = time.time()
        read_params_and_execute()
        total_run_time = time.time() - start_total
        print(f"🏁 All done, total time: {total_run_time:.2f} seconds")
    finally:
        driver.close()
