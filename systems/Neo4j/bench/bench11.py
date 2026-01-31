from neo4j import GraphDatabase
import csv
import time

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"

# PARAM_FILE = "/data/dataset/sf1_bench_param/test.csv"
# PARAM_FILE = "/data/dataset/sf10_bench_param/test.csv"
# PARAM_FILE = "/data/dataset/sf100_bench_param/test.csv"

PARAM_FILE = "params_sf1/complex_11_param.csv"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

execution_times = []
results_count = 0

def execute_query(tx, query):
    """Execute the constructed Cypher query"""
    result = tx.run(query)
    return result.data()

def read_params_and_execute():
    global results_count

    with open(PARAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='|')

        for row in reader:
            """Read parameters and execute queries"""
            node_id = row["id"].strip()
            start_time = int(row["startTime"])   # long in Python
            end_time = int(row["endTime"])       # long in Python

            query = f"""
MATCH p=(p1:Person {{personId: '{node_id}'}})-[:PERSON_GUARANTEE_PERSON*1..5]->(pX:Person)
WHERE all(e IN relationships(p) WHERE {start_time} < e.createTime < {end_time})
UNWIND nodes(p)[1..] AS person
MATCH (person)-[:PERSON_APPLY_LOAN]->(loan:Loan)
RETURN sum(loan.loanAmount) AS sumLoanAmount, count(loan) AS numLoans
"""
            print(f"🔍 Executing query (ID: {node_id})...")
            # print(query)
            # input()

            # Record start time
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

    # Output statistics
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
        print(f"Total Execution Time:  {total_time:.4f} seconds")
        print(f"Average Time per Query: {avg_time:.4f} seconds")
        print(f"Minimum Time per Query: {min_time:.4f} seconds")
        print(f"Maximum Time per Query: {max_time:.4f} seconds")
        print(f"Cumulative Results Returned: {results_count} rows")

        print("="*60)
    else:
        print("⚠️ No successful queries executed.")

if __name__ == "__main__":
    try:
        read_params_and_execute()
    finally:
        driver.close()
