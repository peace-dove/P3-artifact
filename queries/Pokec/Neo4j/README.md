# Pokec Query Templates — Neo4j (Cypher)

Implements path constraints using Neo4j's native path mode keywords (`ACYCLIC`) and Cypher built-in functions. Start/end node IDs are hardcoded in the queries.

## TRAIL

```cypher
CYPHER 25
MATCH p = (x:Entity {{id: '{input_id}'}})-[:Rel*1..5]->(x1) 
RETURN p LIMIT 100000
```

## ACYCLIC

```cypher
CYPHER 25
MATCH p = ACYCLIC (:Entity {{id: '{input_id}'}})-[:Rel*1..5]->(x1)
RETURN p LIMIT 100000
```

## SIMPLE

```cypher
CYPHER 25
MATCH p = (x:Entity {{id: '{input_id}'}})-[:Rel*1..5]->(x1) 
    WHERE allReduce(
    acc = [[], true],
    node IN nodes(p)[0..-1] |
    CASE
        WHEN node IN acc[0] THEN [acc[0], false]
        ELSE [acc[0] + node, true]
    END,
    acc[1] = true
)
RETURN p LIMIT 100000
```
