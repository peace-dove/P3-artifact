# Stack Overflow Query Templates — Neo4j (Cypher)

Uses `CYPHER 25` with quantified path patterns (QPP) and `allReduce()` for temporal constraint evaluation with early pruning. All queries match alternating `P2L`/`L2P` edge patterns via the QPP `(()-[e1:P2L]->()-[e2:L2P]->){1,2}`. Start/end node IDs are parameterized.

## Q5

Single-source temporal reachability with **timestamp ordering**. Each V-pattern pair `(e1, e2)` carries a single `ts` property; `allReduce` tracks the max timestamp of each pair and ensures it precedes the min timestamp of the next pair.

```cypher
CYPHER 25
MATCH p = (u_start:Entity {user_id:{start_id}})
          (()-[e1:P2L]->()-[e2:L2P]->){1,2}
          (u_end:Entity)
WHERE allReduce(
    prev_max = -1,
    i IN range(0, size(e1)-1) |
    CASE WHEN e1[i].ts > e2[i].ts THEN e1[i].ts ELSE e2[i].ts END,
    prev_max = -1 OR prev_max <= CASE WHEN e1[i].ts < e2[i].ts THEN e1[i].ts ELSE e2[i].ts END
)
RETURN p
```

## Q6

Point-to-point variant of Q5 — same timestamp-ordering constraint but with a fixed target node.

```cypher
CYPHER 25
MATCH p = (u_start:Entity {user_id:{start_id}})
          (()-[e1:P2L]->()-[e2:L2P]->){1,2}
          (u_end:Entity {user_id:{end_id}})
WHERE allReduce(
    prev_max = -1,
    i IN range(0, size(e1)-1) |
    CASE WHEN e1[i].ts > e2[i].ts THEN e1[i].ts ELSE e2[i].ts END,
    prev_max = -1 OR prev_max <= CASE WHEN e1[i].ts < e2[i].ts THEN e1[i].ts ELSE e2[i].ts END
)
RETURN p
```

## Q7

Single-source temporal reachability with **interval overlap + sequential ordering**. Each V-pattern pair carries interval properties (`s`, `e`). `allReduce` enforces internal overlap (`max(s1, s2) < min(e1, e2)`) and sequential ordering between consecutive V-patterns (`prev_end <= next e1.s`).

```cypher
CYPHER 25
MATCH p = (u_start:Entity {user_id:{start_id}})
          (()-[e1:P2L]->()-[e2:L2P]->){1,2}
          (u_end:Entity)
WHERE allReduce(
    prev_end = -1,
    i IN range(0, size(e1)-1) |
    e2[i].e,
    max(e1[i].s, e2[i].s) < min(e1[i].e, e2[i].e)
    AND (prev_end = -1 OR prev_end <= e1[i].s)
)
RETURN p
```

## Q8

Point-to-point variant of Q7 — same interval-overlap constraint but with a fixed target node.

```cypher
CYPHER 25
MATCH p = (u_start:Entity {user_id:{start_id}})
          (()-[e1:P2L]->()-[e2:L2P]->){1,2}
          (u_end:Entity {user_id:{end_id}})
WHERE allReduce(
    prev_end = -1,
    i IN range(0, size(e1)-1) |
    e2[i].e,
    max(e1[i].s, e2[i].s) < min(e1[i].e, e2[i].e)
    AND (prev_end = -1 OR prev_end <= e1[i].s)
)
RETURN p
```
