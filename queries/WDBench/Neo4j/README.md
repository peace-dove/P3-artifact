# WDBench Query Templates — Neo4j (Cypher)

Uses `CYPHER 25` with Neo4j's native `ACYCLIC` path mode and `allReduce()` for SIMPLE constraint. TRAIL uses Neo4j's default variable-length semantics (no repeated edges). Start node ID is parameterized. Path length 1..5.

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
