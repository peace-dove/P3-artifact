from neo4j import GraphDatabase
import csv
import time

# Configuration
URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")
DATABASE_NAME = "tugraph_sf10" 
PARAM_FILE = "/data/dataset/sf10/params/complex_1_param.csv"

def execute_and_get_metrics(session, query):
    """
    Execute query and extract server-side timing from Bolt metadata.
    Returns records, plan time, total server time, and raw metadata.
    """
    result = session.run(query)
    records = list(result)
    summary = result.consume()
    meta = summary.metadata
    
    # TuGraph Bolt protocol returns time in milliseconds (ms)
    # result_available_after: Plan generation time
    # result_consumed_after: Total server execution time
    plan_time = summary.result_available_after 
    total_server_time = summary.result_consumed_after

    if plan_time is None:
        plan_time = meta.get('available_after') or meta.get('t_plan')
    if total_server_time is None:
        total_server_time = meta.get('consumed_after') or meta.get('t_exec')
        
    return records, plan_time, total_server_time, meta

def read_params_and_benchmark():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        print(f"Connected to {URI} | Target graph: {DATABASE_NAME}")
        print("Mode: Extract server timing from metadata")

        with open(PARAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            
            for row in reader:
                node_id = row["id"].strip()
                st = row["startTime"]
                et = row["endTime"]

                query = f"""
MATCH p = (acc:Account {{id:{node_id}}})-[e1:transfer *1..3]->(other:Account)<-[e2:signIn]-(medium) 
WHERE isAsc(getMemberProp(e1, 'timestamp'))=true AND 
      head(getMemberProp(e1, 'timestamp')) > {st} AND 
      last(getMemberProp(e1, 'timestamp')) < {et} AND 
      e2.timestamp > {st} AND 
      e2.timestamp < {et} AND 
      medium.isBlocked = true 
RETURN DISTINCT other.id as otherId, 
                length(p)-1 as accountDistance, 
                medium.id as mediumId, 
                medium.type as mediumType 
ORDER BY accountDistance, otherId, mediumId;
"""
                try:
                    start_wall = time.time()
                    with driver.session(database=DATABASE_NAME) as session:
                        recs, p_time, s_time, meta = execute_and_get_metrics(session, query)
                    end_wall = time.time()

                    print(f"ID: {node_id}")
                    print(f"  Server side -> Plan: {p_time}ms | Exec: {s_time}ms")
                    print(f"  Client side -> Wall time: {(end_wall-start_wall)*1000:.2f}ms | Results: {len(recs)} rows")
                    
                    if p_time is None:
                        print(f"  Warning: Time fields not found in metadata. Raw Meta: {meta}")

                except Exception as e:
                    print(f"Failed ID: {node_id} Error: {e}")

if __name__ == "__main__":
    read_params_and_benchmark()
