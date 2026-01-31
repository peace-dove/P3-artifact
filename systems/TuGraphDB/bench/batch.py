from neo4j import GraphDatabase
import time

# Configuration
URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")
DATABASE_NAME = "tugraph_sf10"

PARAM_FILE = "/data/dataset/sf10/params/person_ids.csv"

START_TIME = 1643673600000
END_TIME = 1646092800000

def read_ids_from_file(file_path):
    """Read ID list from text file and convert to integers"""
    ids = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    ids.append(int(line))
                except ValueError:
                    print(f"Skipping invalid ID: {line}")
    return ids

def build_batch_query(id_list, start_time, end_time):
    """Build batch query statement with integer IDs (no quotes)"""
    id_str = ", ".join(str(id_) for id_ in id_list)
    return f"""
MATCH (p:Person)-[e1:own]->(acc:Account) <-[e2:transfer*1..3]-(other:Account) 
WHERE p.id IN [{id_str}] 
  AND isDesc(getMemberProp(e2, 'timestamp')) = true 
  AND head(getMemberProp(e2, 'timestamp')) < {end_time} 
  AND last(getMemberProp(e2, 'timestamp')) > {start_time} 
WITH DISTINCT other 
MATCH (other)<-[e3:deposit]-(loan:Loan) 
WHERE e3.timestamp > {start_time} 
  AND e3.timestamp < {end_time} 
WITH DISTINCT other.id AS otherId, loan.loanAmount AS loanAmount, loan.balance AS loanBalance 
WITH otherId AS otherId, sum(loanAmount) AS sumLoanAmount, sum(loanBalance) AS sumLoanBalance 
RETURN otherId, 
       round(sumLoanAmount * 1000) / 1000 AS sumLoanAmount, 
       round(sumLoanBalance * 1000) / 1000 AS sumLoanBalance 
ORDER BY sumLoanAmount DESC, otherId ASC;
"""

def execute_query(session, query):
    result = session.run(query)
    return result.data()

def run_batch_benchmark():
    print("Starting batch query (int64 IDs + fixed time range)...")
    
    try:
        id_list = read_ids_from_file(PARAM_FILE)
        print(f"Successfully loaded {len(id_list)} IDs (int64)")
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    if not id_list:
        print("No valid IDs found")
        return

    query = build_batch_query(id_list, START_TIME, END_TIME)

    print(query)
    input("Press Enter to continue with query execution...")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        print(f"Connected to {URI} | Graph: {DATABASE_NAME}")
        start_time_sec = time.time()
        try:
            with driver.session(database=DATABASE_NAME) as session:
                records = execute_query(session, query)
            elapsed = time.time() - start_time_sec
            result_count = len(records)
            print(f"Query success | Time: {elapsed:.4f}s | Results: {result_count} rows")

        except Exception as e:
            elapsed = time.time() - start_time_sec
            print(f"Query failed | Time: {elapsed:.4f}s | Error: {e}")
            return

    print("\n" + "=" * 60)
    print("BATCH QUERY COMPLETED (ID type: int64)")
    print("=" * 60)
    print(f"ID Count:              {len(id_list)}")
    print(f"Time Range:            [{START_TIME}, {END_TIME}]")
    print(f"Total Time:            {elapsed:.4f} seconds")
    print(f"Result Count:          {result_count}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_batch_benchmark()
    except KeyboardInterrupt:
        print("\n\nUser interrupted")
    except Exception as e:
        print(f"Exception: {e}")
