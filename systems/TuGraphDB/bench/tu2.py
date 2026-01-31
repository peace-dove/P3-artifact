from neo4j import GraphDatabase
import csv
import time

# Configuration
URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")
DATABASE_NAME = "tugraph_sf100"
PARAM_FILE = "/data/dataset/sf100_bench_param/complex_2_param_res.csv"

execution_times = []
results_count = 0

def execute_query(session, query):
    """Execute query and return data"""
    result = session.run(query)
    return result.data()

def read_params_and_benchmark():
    global results_count

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        print(f"Connected to {URI}, target graph: {DATABASE_NAME}")

        with open(PARAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                node_id = row["id"].strip()
                start_time = int(row["startTime"])
                end_time = int(row["endTime"])

                query = f"""
MATCH (p:Person {{id:{node_id}}})-[e1:own]->(acc:Account) <-[e2:transfer*1..3]-(other:Account) 
WHERE isDesc(getMemberProp(e2, 'timestamp'))=true AND 
      head(getMemberProp(e2, 'timestamp')) < {end_time} AND 
      last(getMemberProp(e2, 'timestamp')) > {start_time} 
WITH DISTINCT other 
MATCH (other)<-[e3:deposit]-(loan:Loan) 
WHERE e3.timestamp > {start_time} AND 
      e3.timestamp < {end_time} 
WITH DISTINCT other.id AS otherId, loan.loanAmount AS loanAmount, loan.balance AS loanBalance 
WITH otherId AS otherId, sum(loanAmount) as sumLoanAmount, sum(loanBalance) as sumLoanBalance 
RETURN otherId, round(sumLoanAmount * 1000) / 1000 as sumLoanAmount, round(sumLoanBalance * 1000) / 1000 as sumLoanBalance 
ORDER BY sumLoanAmount DESC, otherId ASC;
"""

                print(f"Executing query | ID: {node_id}")

                start_time_sec = time.time()
                try:
                    with driver.session(database=DATABASE_NAME) as session:
                        records = execute_query(session, query)
                    elapsed = time.time() - start_time_sec
                    execution_times.append(elapsed)
                    results_count += len(records)

                    print(f"Success | Time: {elapsed:.4f}s | Results: {len(records)} rows")

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
        print("BENCHMARK COMPLETED (Neo4j Driver)")
        print("=" * 60)
        print(f"Connection URI:        {URI}")
        print(f"Target Graph:          {DATABASE_NAME}")
        print(f"Total Queries:         {total_queries}")
        print(f"Total Time:            {total:.4f} seconds")
        print(f"Average Time:          {avg:.4f} seconds")
        print(f"Min Time:              {mini:.4f} seconds")
        print(f"Max Time:              {maxi:.4f} seconds")
        print(f"Total Records:         {results_count} rows")
        print("=" * 60)
    else:
        print("No queries executed successfully.")

if __name__ == "__main__":
    print("Starting performance test...")
    try:
        read_params_and_benchmark()
    except KeyboardInterrupt:
        print("\n\nUser interrupted.")
    except Exception as e:
        print(f"Program error: {e}")
