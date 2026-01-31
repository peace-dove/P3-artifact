import kuzu as kz
import time
import csv

# Connect to existing database
db = kz.Database("kuzu_pokec")
conn = kz.Connection(db)

OUTPUT_CSV = "acyclic_id_max_5.csv"

# Change code to read user ids here
ids = range(1, 101) # example here

with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'time'])

times = []

print("Running queries for id 1 to 100...")

for user_id in ids:
    query = f"""
        MATCH p = (x:User {{id: '{user_id}'}})-[:Rel* 1..5]->(x1:User) 
        WHERE is_acyclic(p) 
        RETURN p 
    """

    start = time.perf_counter()
    result = conn.execute(query)
    # Consume result to ensure query execution
    count_val = result.get_next()[0] if result.has_next() else 0
    
    # while result.has_next():
    #     print(result.get_next())
    
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
