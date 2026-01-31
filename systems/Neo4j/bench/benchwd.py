from neo4j import GraphDatabase
import time

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
QUERY_FILE = "wd_query/test_part.txt"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

execution_times = []
results_count = 0
failed_queries = []

def execute_query(tx, query):
    result = tx.run(query)
    return result.data()

def read_queries_and_execute():
    global results_count

    print(f"📂 start reading: {QUERY_FILE}")
    try:
        with open(QUERY_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"❌ Error: File not found '{QUERY_FILE}'")
        return

    total_queries = len(lines)
    print(f"✅ Loaded {total_queries} queries\n")
    for line in lines:
        parts = line.split(',', 1)

        query_id, cypher_query = parts[0].strip(), parts[1].strip()

        print(f"🔍 Executing query ID: {query_id} ...")
        # print(f"📝 Query content:\n{cypher_query}\n")

        start_time = time.time()
        try:
            with driver.session() as session:
                records = session.read_transaction(execute_query, cypher_query)
            elapsed = time.time() - start_time
            execution_times.append(elapsed)
            result_len = len(records)
            results_count += result_len

            print(f"✅ Success | Time: {elapsed:.4f}s | Results: {result_len} rows\n")

        except Exception as e:
            elapsed = time.time() - start_time
            execution_times.append(elapsed)
            failed_queries.append(query_id)
            print(f"❌ Failure | Time: {elapsed:.4f}s | Error: {e}\n")

    # Output final statistics
    if execution_times:
        total_time = sum(execution_times)
        avg_time = total_time / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)

        print("=" * 60)
        print("📈 Query Execution Completed (Summary Statistics)")
        print("=" * 60)
        print(f"Total Queries Executed:   {len(execution_times)}")
        print(f"Successful Executions:    {len(execution_times) - len(failed_queries)}")
        print(f"Failed Executions:        {len(failed_queries)}")
        if failed_queries:
            print(f"Failed Query IDs:       {', '.join(failed_queries)}")
        print(f"Total Execution Time:         {total_time:.4f} seconds")
        print(f"Average Time per Query:       {avg_time:.4f} seconds")
        print(f"Minimum Time per Query:       {min_time:.4f} seconds")
        print(f"Maximum Time per Query:       {max_time:.4f} seconds")
        print(f"Cumulative Results Returned: {results_count} rows")
        print("=" * 60)
    else:
        print("⚠️ No successful queries executed.")

if __name__ == "__main__":
    try:
        read_queries_and_execute()
    finally:
        driver.close()
