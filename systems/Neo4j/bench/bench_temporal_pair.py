from neo4j import GraphDatabase
import time
import csv
import os

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
INPUT_PAIRS_FILE = "temporal/pairs.txt"
OUTPUT_CSV = "temporal/pair.csv"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def run_connectivity_benchmark():
    print("🚀 Starting [Temporal Pair Connectivity] benchmark...")
    
    # Check if input file exists
    if not os.path.exists(INPUT_PAIRS_FILE):
        print(f"❌ Error: Input file not found {INPUT_PAIRS_FILE}")
        return

    with open(INPUT_PAIRS_FILE, 'r') as f_in, \
         open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        
        writer = csv.writer(csvfile)
        writer.writerow(['start_id', 'end_id', 'time_seconds', 'is_connected'])

        total_time = 0
        success_count = 0

        for line in f_in:
            parts = line.strip().split()
            if len(parts) < 2: continue
            
            start_id, end_id = parts[0], parts[1]

            # Core Cypher query
            # Add LIMIT 1, as long as one path meeting the temporal requirements is found, it is considered connected
            cypher_query = f"""
                MATCH (u_start:User {{user_id: '{start_id}'}}), (u_end:User {{user_id: '{end_id}'}})
                MATCH p = (u_start)-[:P2L|L2P*6..6]->(u_end)
                WHERE ALL(i IN range(0, size(relationships(p))-1) WHERE 
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
                RETURN count(p) > 0 AS connected 
                LIMIT 1
            """

            start_time = time.time()
            try:
                with driver.session() as session:
                    result = session.run(cypher_query)
                    record = result.single()
                    is_connected = 1 if record and record["connected"] else 0
                
                elapsed = time.time() - start_time
                writer.writerow([start_id, end_id, f"{elapsed:.6f}", is_connected])
                
                total_time += elapsed
                success_count += 1
                
                status = "🔗 Connected" if is_connected else "🚫 Not Connected"
                print(f"ID {start_id:>3s} -> {end_id:>3s} | {status} | Time: {elapsed:.4f}s")

            except Exception as e:
                elapsed = time.time() - start_time
                writer.writerow([start_id, end_id, f"{elapsed:.6f}", -1])
                print(f"❌ ID {start_id} -> {end_id} | Error: {str(e)[:50]}...")

        print("\n" + "=" * 60)
        print(f"📊 Benchmark completed. Average time: {total_time/success_count:.4f}s" if success_count > 0 else "Benchmark failed")
        print(f"Results saved to: {OUTPUT_CSV}")
if __name__ == "__main__":
    try:
        run_connectivity_benchmark()
    finally:
        driver.close()
