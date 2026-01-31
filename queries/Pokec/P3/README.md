# Pokec Query Templates — P3 (GQL)

Uses GQL standard path mode keywords (`ACYCLIC`, `SIMPLE`, `TRAIL`) directly in the MATCH clause. Start node ID is hardcoded in the queries.

> Remark: The query statements of P3 and GU are identical.

## TRAIL

```sql
MATCH p = TRAIL (:PokecEntity{id:'{user_id}'})-[e:PokecRel]->{1,5}(x1:PokecEntity)
RETURN p;
```

## ACYCLIC

```sql
MATCH p = ACYCLIC (:PokecEntity{id:'{user_id}'})-[e:PokecRel]->{1,5}(x1:PokecEntity)
RETURN p;
```

## SIMPLE

```sql
MATCH p = SIMPLE (:PokecEntity{id:'{user_id}'})-[e:PokecRel]->{1,5}(x1:PokecEntity)
RETURN p;
```
