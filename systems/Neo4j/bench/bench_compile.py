from neo4j import GraphDatabase
import csv
import time

URI = "neo4j://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "neo4j"
PARAM_FILE = "params_sf1/complex_1_param.csv"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

execution_times = []        # result_consumed_after
compilation_times = []      # result_available_after
results_count = 0
failed_queries = []

def execute_query(session, query):
    result = session.run(query)
    records = list(result)
    summary = result.consume()
    return records, summary

def read_params_and_execute():
    global results_count

    print(f"📂: {PARAM_FILE}")
    try:
        with open(PARAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            rows = list(reader)
    except FileNotFoundError:
        print(f"❌  '{PARAM_FILE}'")
        return
    except Exception as e:
        print(f"❌ : {e}")
        return

    total_queries = len(rows)
    print(f"✅ load {total_queries} \n")

    for row in rows:
        node_id = row["id"].strip()
        start_time = int(row["startTime"])
        end_time = int(row["endTime"])

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

        print(f"🔍 query (ID: {node_id})...")

        try:
            with driver.session() as session:
                records, summary = execute_query(session, query)

            compile_time = summary.result_available_after / 1000.0
            total_time = summary.result_consumed_after / 1000.0

            compilation_times.append(compile_time)
            execution_times.append(total_time)
            result_len = len(records)
            results_count += result_len

            print(f"✅ success | ")
            print(f"   ├─ compile time: {compile_time:.4f}s")
            print(f"   ├─ total time:   {total_time:.4f}s")
            print(f"   └─ results:      {result_len}\n")

        except Exception as e:
            elapsed = time.time() - time.time()
            start_fail = time.time()
            try:
                with driver.session() as session:
                    session.read_transaction(lambda tx: tx.run(query).data())
            except:
                pass
            elapsed = time.time() - start_fail
            execution_times.append(elapsed)
            compilation_times.append(elapsed)
            failed_queries.append(node_id)
            print(f"❌ failed | elapsed: {elapsed:.4f}s | error: {e}\n")

    if execution_times:
        total_compile = sum(compilation_times)
        avg_compile = total_compile / len(compilation_times)
        min_compile = min(compilation_times)
        max_compile = max(compilation_times)

        total_exec = sum(execution_times)
        avg_exec = total_exec / len(execution_times)
        min_exec = min(execution_times)
        max_exec = max(execution_times)

        successful_count = len(execution_times) - len(failed_queries)

        print("\n" + "=" * 70)
        print("📈 query execution completed (summary)")
        print("=" * 70)
        print(f"total queries executed:     {len(execution_times)}")
        print(f"successful executions:      {successful_count}")
        print(f"failed executions:          {len(failed_queries)}")
        if failed_queries:
            print(f"failed query IDs:         {', '.join(failed_queries)}")
        print()
        print("⏱️ compile time statistics (query optimization phase)")
        print(f"  total compile time:         {total_compile:.4f} seconds")
        print(f"  average compile time:       {avg_compile:.4f} seconds")
        print(f"  minimum compile time:       {min_compile:.4f} seconds")
        print(f"  maximum compile time:       {max_compile:.4f} seconds")
        print()
        print("🎯 execution time statistics (end-to-end total time)")
        print(f"  total execution time:         {total_exec:.4f} seconds")
        print(f"  average execution time:       {avg_exec:.4f} seconds")
        print(f"  minimum execution time:       {min_exec:.4f} seconds")
        print(f"  maximum execution time:       {max_exec:.4f} seconds")
        print()
        print(f"total results returned:       {results_count} rows")
        print("=" * 70)
    else:
        print("⚠️ no queries were successfully executed.\n")


if __name__ == "__main__":
    try:
        read_params_and_execute()
    finally:
        driver.close()
