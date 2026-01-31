# Stack Overflow Query Templates — P3 (GQL with SW)

Uses the GQL/SW (sliding-window) syntax to express temporal constraints declaratively. All queries match alternating `Rel` edges with even-length paths (1..4 hops). Start/end node IDs are hardcoded in the queries.

> Remark: For GU, we implement the UDFs for timestamp ordering.

## Q5

Single-source temporal reachability with **timestamp ordering**. `SW(2)` slides a window of size 2 over consecutive edges; the constraint enforces that each edge's `ts` is less than the next.

```sql
MATCH p = (n1:Entity{id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WITH SW(2) ON p AS pp 
WHERE length(p) % 2 == 0 AND
      relationships(pp)[0].ts < relationships(pp)[1].ts 
RETURN p
```

## Q6

Point-to-point variant of Q5 — same timestamp-ordering constraint but with a fixed target node (`n2.id = {end_id}`).

```sql
MATCH p = (n1:Entity{id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WITH SW(2) ON p AS pp 
WHERE n2.id = {end_id} AND length(p) % 2 == 0 AND
      relationships(pp)[0].ts < relationships(pp)[1].ts 
RETURN p
```

## Q7

Single-source temporal reachability with **interval overlap + sequential ordering**. Uses two sliding windows: `SW(2, step = 2)` for V-pattern internal overlap (`max(s1, s2) < min(e1, e2)`) and `SW(4, step = 2)` for sequential ordering between consecutive V-patterns (`pp1[1].e <= pp1[2].s`).

```sql
MATCH p = (n1:Entity {id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WITH SW(4, step = 2) on p as pp1, SW(2, step = 2) ON p AS pp2 
WHERE length(p) % 2 == 0 AND
      max(relationships(pp2)[0].s, relationships(pp2)[1].s) < min(relationships(pp2)[0].e, relationships(pp2)[1].e) AND 
      relationships(pp1)[1].e <= relationships(pp1)[2].s
RETURN p
```

## Q8

Point-to-point variant of Q7 — same interval-overlap constraint but with a fixed target node (`n2.id = {end_id}`).

```sql
MATCH p = (n1:Entity {id:{start_id}})-[e1:Rel]->{1,4}(n2:Entity) 
WITH SW(4, step = 2) on p as pp1, SW(2, step = 2) ON p AS pp2 
WHERE n2.id = {end_id} AND length(p) % 2 == 0 AND
      max(relationships(pp2)[0].s, relationships(pp2)[1].s) < min(relationships(pp2)[0].e, relationships(pp2)[1].e) AND 
      relationships(pp1)[1].e <= relationships(pp1)[2].s
RETURN p
```
