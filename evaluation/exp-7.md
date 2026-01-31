# Exp-7: Case Study

The following queries are the template for FinBench Q1 / WDBench ACYCLIC.

> Note: The two case studies are run independently from Exp-1/Exp-2 with hop ranges extended to expose the per-loop pruning behavior.

## Query TCR1 on FinBench

> Tested with hop range extended to 1--5.

```SQL
-- Q_TCR1: 1--5 hop Transfer paths with asc timestamps
MATCH p = (s:Account)-[e:Transfer]->{1,5} (t:Account),
          (t)<-[e1:SignIn]-(med:Medium)
WITH SW(2) ON p AS pp
WHERE pp[0].ts < pp[1].ts -- PRP predicate via GQL/SW
  AND s.id = '46726495401431756'
  AND med.isBlocked = True
  AND e1.ts > '2022-08-01' AND e1.ts < '2022-09-26'
  AND head(p).ts > '2022-08-01' AND last(p).ts < '2022-09-26'
RETURN distinct t.id AS dstId, length(p) AS accDst,
                med.id AS mediumId, med.type AS mediumType
ORDER BY accDst, dstId, mediumId;
```

Surviving Path Count:

|  | loop1 | loop2 | loop3 | loop4 | loop5 | filter |
| --- | --- | --- | --- | --- | --- | --- |
| P3 | 3 | 11 | 29 | 59 | 107 | 5 |
| GU | 3 | 13 | 36 | 96 | 219 | 5 |


## Query Acyclic on WDBench

> Tested on a single hand-picked source vertex with hop range 3--7.

```SQL
-- Q_ACY: Acyclic paths of length 3--7 from a source.
MATCH p = ACYCLIC (:Entity {id: 'Q23794244'})
                  -[:Rel]->{3,7} (:Entity)
RETURN p;
```

Surviving Path Count:

|  | loop3 | loop4 | loop5 | loop6 | loop7 | filter |
| --- | --- | --- | --- | --- | --- | --- |
| P3 | 12 | 16 | 21 | 38 | 49 | - |
| GU | 15 | 20 | 35 | 67 | 108 | 49 |

> Remark: P3's filter column shows `-` because P3's on-the-fly pruning has already enforced the acyclic constraint during path expansion — no post-filter operator is needed. GU, without PRP optimization, must apply a post-filter after full path enumeration, reducing 108 surviving paths to the 49 valid acyclic paths.
