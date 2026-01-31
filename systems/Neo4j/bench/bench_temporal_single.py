from neo4j import GraphDatabase
import time
import csv
import os

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
OUTPUT_CSV = "temporal/single_temporal.csv"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def execute_query(tx, query):
    result = tx.run(query)
    return result.data()

def execute_protected_query(tx, query):
    result = tx.run(query)
    return result.data()

def run_benchmark():
    print("🚀 Starting [Temporal Path] benchmark...")
    print(f"Test depth: 6 steps (Person-Mail-Person-Mail-Person-Mail-Person)")
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'time_seconds', 'result_count'])

        total_time = 0
        total_results = 0
        failed_ids = []

        for input_id in range(1, 101):
            cypher_query = f"""
                MATCH p = (u_start:User {{user_id: '{input_id}'}})-[:P2L|L2P*2..4]->(u_end:User)
                WHERE length(p) % 2 = 0
                AND ALL(i IN range(0, size(relationships(p))-1) WHERE 
                    (i % 2 = 0 AND type(relationships(p)[i]) = 'P2L') OR 
                    (i % 2 = 1 AND type(relationships(p)[i]) = 'L2P')
                )
                AND REDUCE(acc = {{valid: true, last_e: -1}}, i IN range(0, size(relationships(p))-1, 2) |
                    CASE
                        WHEN NOT acc.valid THEN acc
                        WHEN acc.last_e <> -1 AND acc.last_e > (
                            CASE 
                                WHEN relationships(p)[i].ts < relationships(p)[i+1].ts 
                                THEN relationships(p)[i].ts 
                                ELSE relationships(p)[i+1].ts 
                            END
                        ) THEN {{valid: false, last_e: -1}}
                        ELSE {{
                            valid: true, 
                            last_e: (
                                CASE 
                                    WHEN relationships(p)[i].ts > relationships(p)[i+1].ts 
                                    THEN relationships(p)[i].ts 
                                    ELSE relationships(p)[i+1].ts 
                                END
                            )
                        }}
                    END
                ).valid
                RETURN p
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
                
                print(f"✅ ID {input_id:2d} | Time: {elapsed:.4f}s | Results: {result_count} rows")

            except Exception as e:
                elapsed = time.time() - start_time
                failed_ids.append(input_id)
                writer.writerow([input_id, f"{elapsed:.6f}", -1])
                print(f"❌ ID {input_id:2d} | Time: {elapsed:.4f}s | Error: {str(e)[:50]}...")


        # Summary statistics
        success_count = 100 - len(failed_ids)
        avg_time = total_time / success_count if success_count > 0 else 0

        print("\n" + "=" * 60)
        print("📊 Benchmark completed summary")
        print("-" * 60)
        print(f"Number of test samples: 100")
        print(f"Number of successes: {success_count}")
        print(f"Number of failures: {len(failed_ids)}")
        if failed_ids: print(f"List of failed IDs: {failed_ids}")
        print(f"Average time: {avg_time:.4f} seconds/query")
        print(f"Total results: {total_results}")
        print(f"Results saved to: {OUTPUT_CSV}")
        print("=" * 60)

if __name__ == "__main__":
    try:
        run_benchmark()
    finally:
        driver.close()
        print("🔌 Neo4j connection closed")
