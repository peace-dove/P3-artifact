# Pokec Query Templates — Kuzu (Cypher)

Uses Kuzu predicate functions (`is_acyclic`, `is_trail`) and inline path modes (`ACYCLIC`). `{user_id}` placeholder is substituted from `../params/params-acyclic.txt`.

## TRAIL

```cypher
MATCH p = (x:User {id: '{user_id}'})-[:Rel* 1..5]->(x1:User)
WHERE is_trail(p)
RETURN p
```

## ACYCLIC

```cypher
MATCH p = (x:User {id: '{user_id}'})-[:Rel* 1..5]->(x1:User)
WHERE is_acyclic(p)
RETURN p
```

## SIMPLE

```cypher
MATCH p = (x:User {id: '{user_id}'})-[e:Rel* ACYCLIC 1..5]->(y:User)
WHERE NOT ( (x in list_slice(nodes(p), 1, -1)) OR (y in list_slice(nodes(p), 1, -1)) )
RETURN p
```
