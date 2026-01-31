# WDBench Query Templates — Kuzu (Cypher)

Uses Kuzu's built-in path constraint functions (`is_trail`, `is_acyclic`) and list slicing. Start node ID is parameterized. Path length 1..5.

## TRAIL

```cypher
MATCH p = (x:WDEntity {{id: '{id}'}})-[:Rel* 1..5]->(x1:WDEntity) 
WHERE is_trail(p) 
RETURN p 
```

## ACYCLIC

```cypher
MATCH p = (x:WDEntity {{id: '{id}'}})-[:Rel* 1..5]->(x1:WDEntity) 
WHERE is_acyclic(p) 
RETURN p 
```

## SIMPLE

```cypher
MATCH p = (x:WDEntity {{id: '{id}'}})-[e:Rel* ACYCLIC 1..5]->(y:WDEntity) 
WHERE NOT ( (x in list_slice(nodes(p), 1, -1)) OR (y in list_slice(nodes(p), 1, -1)) ) 
RETURN p
```
