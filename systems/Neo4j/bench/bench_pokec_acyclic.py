from neo4j import GraphDatabase
import time
import csv

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
OUTPUT_CSV = "pokec_query/acyclic_temp_max_3.csv"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def execute_query(tx, query):
    result = tx.run(query)
    return result.data()

def run_benchmark():    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'time_seconds', 'result_count'])

        total_time = 0
        total_results = 0
        failed_ids = []

        for input_id in range(1, 101):
            cypher_query = f"""
                CYPHER 25
                MATCH p = ACYCLIC (:Entity {{id: '{input_id}'}})-[:Rel*1..3]->(x1)
                RETURN p LIMIT 100000
            """

            start_time = time.time()
            try:
                with driver.session() as session:
                    records = session.read_transaction(execute_protected_query, cypher_query)
                elapsed = time.time() - start_time
                result_count = len(records)
                
                writer.writerow([input_id, f"{elapsed:.6f}", result_count])
                
                total_time += elapsed
                total_results += result_count
                
                print(f"✅ ID {input_id:2d} | elapsed: {elapsed:.4f}s | results: {result_count} rows")

            except Exception as e:
                elapsed = time.time() - start_time
                failed_ids.append(input_id)
                writer.writerow([input_id, f"{elapsed:.6f}", -1])
                print(f"❌ ID {input_id:2d} | elapsed: {elapsed:.4f}s | error: {str(e)[:50]}...")

        success_count = 100 - len(failed_ids)
        avg_time = total_time / success_count if success_count > 0 else 0

        print("\n" + "=" * 60)
        print("📊 Benchmark completed")
        print("=" * 60)
        print(f"Success: {success_count} / 100")
        print(f"Failures: {len(failed_ids)} (IDs: {failed_ids})")
        print(f"Total time: {total_time:.4f} seconds")
        print(f"Average time: {avg_time:.4f} seconds/query")
        print(f"Total results: {total_results}")
        print(f"Detailed data saved to: {OUTPUT_CSV}")
        print("=" * 60)

def execute_protected_query(tx, query):
    result = tx.run(query)
    return result.data()

if __name__ == "__main__":
    try:
        run_benchmark()
    finally:
        driver.close()
        print("🔌 Neo4j connection closed")
