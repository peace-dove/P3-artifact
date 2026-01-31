import kuzu as kz

# 1. Create or open a database
# The database file will be created in the specified directory
db = kz.Database("kuzu_pokec")

# 2. Establish a connection
conn = kz.Connection(db)

# 3. Execute a Cypher query (DDL)
conn.execute("CREATE NODE TABLE User(id STRING, PRIMARY KEY(id))")
conn.execute("CREATE REL TABLE Rel(FROM User TO User)")

conn.execute("COPY User FROM './dataset/id.csv'")
conn.execute("COPY Rel FROM './dataset/relationships.csv'")

# result = conn.execute("""
#     MATCH (a:User)-[e:Rel]->(b:User) 
#     RETURN a.id, b.id LIMIT 10
# """)

# while result.has_next():
#     print(result.get_next())
