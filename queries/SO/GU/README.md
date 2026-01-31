# Stack Overflow Query Templates — GU (GQL w/o SW)

Uses UDFs (`isAsc`, `isAscInterval`) to express temporal constraints. All queries match alternating `Rel` edges with even-length paths (1..4 hops). Start/end node IDs are hardcoded in the queries.

> Remark: GU uses UDFs instead of sliding windows for temporal constraint evaluation.

## Q5

Single-source temporal reachability with **timestamp ordering**. Uses `isAsc` UDF to enforce that each edge's `ts` is less than the next.

```sql
MATCH p = (n1:Entity{id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WHERE length(p) % 2 == 0
      AND isAsc(relationships(p), 0) = true
RETURN p
```

## Q6

Point-to-point variant of Q5 — same timestamp-ordering constraint but with a fixed target node (`n2.id = {end_id}`).

```sql
MATCH p = (n1:Entity{id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WHERE n2.id = {end_id}
      AND length(p) % 2 == 0
      AND isAsc(relationships(p), 0) = true
RETURN p
```

## Q7

Single-source temporal reachability with **interval overlap + sequential ordering**. Uses `isAscInterval` UDF to enforce V-pattern internal overlap (`max(s1, s2) < min(e1, e2)`) and sequential ordering between consecutive V-patterns (`prev.e <= next.s`).

```sql
MATCH p = (n1:Entity {id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WHERE length(p) % 2 == 0
      AND isAscInterval(relationships(p)) = True
RETURN p
```

## Q8

Point-to-point variant of Q7 — same interval-overlap constraint but with a fixed target node (`n2.id = {end_id}`).

```sql
MATCH p = (n1:Entity {id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WHERE n2.id = {end_id}
      AND length(p) % 2 == 0
      AND isAscInterval(relationships(p)) = True
RETURN p
```
