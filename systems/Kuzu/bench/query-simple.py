import kuzu as kz
import time
import csv

# Connect to existing database
db = kz.Database("kuzu_pokec")
conn = kz.Connection(db)

OUTPUT_CSV = "simple_id_max_3.csv"

# Change code to read user ids here
ids = range(1, 101) # example here

# Write CSV header
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'time'])

times = []

print("Running queries for id 1 to 100...")

for user_id in ids:
    query = f"""
        MATCH p = (x:User {{id: '{user_id}'}})-[e:Rel* ACYCLIC 1..3]->(y:User) 
        WHERE NOT ( (x in list_slice(nodes(p), 1, -1)) OR (y in list_slice(nodes(p), 1, -1)) ) 
        RETURN p
    """

    start = time.perf_counter()
    result = conn.execute(query)
    # Consume result to ensure query execution
    count_val = result.get_next()[0] if result.has_next() else 0
    end = time.perf_counter()
    
    elapsed_ms = (end - start) * 1000  # Convert to milliseconds
    times.append(elapsed_ms)
    
    with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, f"{elapsed_ms:.4f}"])
    
    print(f"id={user_id}, time={elapsed_ms:.4f} ms")

avg_time = sum(times) / len(times)
print("\n" + "="*50)
print(f"✅ Average time for id 1~100: {avg_time:.4f} ms")
print(f"📁 Results saved to: {OUTPUT_CSV}")
