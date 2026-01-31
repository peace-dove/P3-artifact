# Stack Overflow Query Templates — TuGraphDB (Cypher with helpers)

Uses TuGraphDB helper functions (`getMemberProp`, `isAsc`). Start/end node IDs are parameterized. All queries match alternating `P2L`/`L2P` edge patterns with even-length paths (1..4 hops).

## Q5

Single-source temporal reachability with **timestamp ordering**. `isAsc` over all edge timestamps ensures each edge's `ts` is strictly less than the next.

```cypher
MATCH p = (u_start:User {user_id:{start_id}})-[e:P2L|L2P*1..4]->(u_end:User)
WHERE length(p) % 2 = 0
  AND isAsc(getMemberProp(e, 'ts'))=true
RETURN p
```

## Q6

Point-to-point variant of Q5 — same timestamp-ordering constraint but with a fixed target node.

```cypher
MATCH p = (u_start:User {user_id:{start_id}})-[e:P2L|L2P*1..4]->(u_end:User {user_id:{end_id}})
WHERE length(p) % 2 = 0
  AND isAsc(getMemberProp(e, 'ts'))=true
RETURN p
```
