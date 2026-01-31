from neo4j import GraphDatabase
import csv
import time

# Configuration
URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")
DATABASE_NAME = "tugraph_sf10"
PARAM_FILE = "/data/dataset/sf10/params/complex_1_param.csv"

execution_times = []
results_count = 0

def execute_query(session, query):
    result = session.run(query)
    return result.data()

def read_params_and_benchmark():
    global results_count

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        print(f"Connected to {URI}, database: {DATABASE_NAME}")

        with open(PARAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                node_id = row["id"].strip()
                start_time = int(row["startTime"])
                end_time = int(row["endTime"])

                query = f"""
MATCH p = (acc:Account {{id:{node_id}}})-[e1:transfer *1..3]->(other:Account)<-[e2:signIn]-(medium) 
WHERE isAsc(getMemberProp(e1, 'timestamp'))=true AND 
      head(getMemberProp(e1, 'timestamp')) > {start_time} AND 
      last(getMemberProp(e1, 'timestamp')) < {end_time} AND 
      e2.timestamp > {start_time} AND 
      e2.timestamp < {end_time} AND 
      medium.isBlocked = true 
RETURN DISTINCT other.id as otherId, 
                length(p)-1 as accountDistance, 
                medium.id as mediumId, 
                medium.type as mediumType 
ORDER BY accountDistance, otherId, mediumId;
"""

                print(f"Executing query | ID: {node_id}")

                start_time_sec = time.time()
                try:
                    with driver.session(database=DATABASE_NAME) as session:
                        records = execute_query(session, query)
                    elapsed = time.time() - start_time_sec
                    execution_times.append(elapsed)
                    results_count += len(records)

                    print(f"Success | Time: {elapsed:.4f}s | Results: {len(records)}")

                except Exception as e:
                    elapsed = time.time() - start_time_sec
                    execution_times.append(elapsed)
                    print(f"Failed | Time: {elapsed:.4f}s | Error: {e}")

    if execution_times:
        total = sum(execution_times)
        avg = total / len(execution_times)
        mini = min(execution_times)
        maxi = max(execution_times)
        total_queries = len(execution_times)

        print("\n" + "=" * 60)
        print("BENCHMARK COMPLETED")
        print("=" * 60)
        print(f"URI:               {URI}")
        print(f"Database:          {DATABASE_NAME}")
        print(f"Total queries:     {total_queries}")
        print(f"Total time:        {total:.4f} s")
        print(f"Average time:      {avg:.4f} s")
        print(f"Min time:          {mini:.4f} s")
        print(f"Max time:          {maxi:.4f} s")
        print(f"Total results:     {results_count}")
        print("=" * 60)
    else:
        print("No queries executed successfully.")

if __name__ == "__main__":
    print("Starting benchmark...")
    try:
        read_params_and_benchmark()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

