# WDBench Query Templates — GU (GQL)

Uses GQL standard path mode keywords (`TRAIL`, `ACYCLIC`, `SIMPLE`) directly in the MATCH clause. Start node ID is hardcoded in the queries.

> Remark: The query statements of P3 and GU are identical.

## TRAIL

```sql
MATCH p = TRAIL (:WDEntity{id:'{start_id}'})-[e:WDRel]->{1,5}(x1:WDEntity) 
RETURN p;
```

## ACYCLIC

```sql
MATCH p = ACYCLIC (:WDEntity{id:'{start_id}'})-[e:WDRel]->{1,5}(x1:WDEntity) 
RETURN p;
```

## SIMPLE

```sql
MATCH p = SIMPLE (:WDEntity{id:'{start_id}'})-[e:WDRel]->{1,5}(x1:WDEntity) 
RETURN p;
```
