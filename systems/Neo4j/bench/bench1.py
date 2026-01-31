from neo4j import GraphDatabase
import csv
import time

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
# PARAM_FILE = "/data/dataset/sf100_bench_param/test.csv"
PARAM_FILE = "params_sf10/1.csv"
# PARAM_FILE = "params_sf3/complex_1_param.csv"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

execution_times = []
results_count = 0

def execute_query(tx, query):
    result = tx.run(query)
    return result.data()

def print_plan(plan, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{plan.operator_type}")
    if plan.arguments:
        for key, value in plan.arguments.items():
            if key not in ("planner", "version", "KeyNames"):
                print(f"{prefix}  {key}: {value}")
    for child in plan.children:
        print_plan(child, indent + 1)

def read_params_and_execute():
    global results_count

    with open(PARAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            node_id = row["id"].strip()
            start_time = int(row["startTime"])   # long in Python
            end_time = int(row["endTime"])       # long in Python

            query = f"""
MATCH
  p=(account:Account {{accountId: '{node_id}'}})-[edge1:ACCOUNT_TRANSFER_ACCOUNT*1..3]->(other:Account),
  (other)<-[edge2:MEDIUM_SIGNIN_ACCOUNT]-(medium:Medium {{isBlocked: true}})
WITH p, [e IN relationships(p) | e.createTime] AS ts, other, medium
WHERE 
      reduce(curr = head(ts), x IN tail(ts) | CASE WHEN curr < x THEN x ELSE 9223372036854775807 END) <> 9223372036854775807
  AND all(e IN edge1 WHERE {start_time} < e.createTime < {end_time})
  AND {start_time} < edge2.createTime < {end_time}
RETURN 
    other.accountId AS otherId, 
    length(p) AS accountDistance, 
    medium.mediumId AS mediumId, 
    medium.mediumType AS mediumType
ORDER BY accountDistance ASC;
"""
            print(f"🔍 Querying (ID: {node_id})...")

            start_time_sec = time.time()

            try:
                with driver.session() as session:
                    records = session.read_transaction(execute_query, query)
                elapsed = time.time() - start_time_sec
                execution_times.append(elapsed)
                results_count += len(records)
                print(f"✅ Success | Time: {elapsed:.4f}s | Results: {len(records)} rows")

            except Exception as e:
                elapsed = time.time() - start_time_sec
                execution_times.append(elapsed)
                print(f"❌ Failure | Time: {elapsed:.4f}s | Error: {e}")
                

    if execution_times:
        total_time = sum(execution_times)
        avg_time = total_time / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        total_queries = len(execution_times)

        print("\n" + "="*60)
        print("📈 Query Execution Completed (Summary Statistics)")
        print("="*60)
        print(f"Total Queries Executed: {total_queries}")
        print(f"Total Execution Time:   {total_time:.4f} seconds")
        print(f"Average Time per Query: {avg_time:.4f} seconds")
        print(f"Shortest Query Time:    {min_time:.4f} seconds")
        print(f"Longest Query Time:     {max_time:.4f} seconds")
        print(f"Total Results Returned: {results_count} rows")
        print("="*60)
    else:
        print("⚠️ No queries were successfully executed.")

if __name__ == "__main__":
    try:
        read_params_and_execute()
    finally:
        driver.close()
