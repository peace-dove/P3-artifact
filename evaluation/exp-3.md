# Exp-3: Memory Usage

### Aggregate (hop 3–7)

Setup: Pokec, hop 3–7.

> Remark: Base memory overhead has been subtracted from all values: P3 and GU = 2858 MB, Kuzu = 6883 MB, Neo4j = 4571 MB, PathFinder = 2267 MB. The numbers below are averages across hop 3–7, reflecting query-execution-only memory consumption.

| | TRAIL | ACYCLIC | SIMPLE |
| --- | --- | --- | --- |
| P3      | 2267 | 1983 | 2078 |
| GU   | 2759 | 2691 | 2735 |
| Kuzu       | 14706 | 14034 | 14382 |
| Neo4j      | 7840 | 5789 | 6822 |
| PathFinder | 3525 | 3192 | 3396 |

### By hop length (hop 3, 5, 7)

> Remark: Values are averaged across TRAIL, ACYCLIC, and SIMPLE.

| | Hop 3 | Hop 5 | Hop 7 |
| --- | --- | --- | --- |
| P3     | 718  | 1893 | 4375 |
| GU        | 1027  | 2473 | 7121 |
| Kuzu       | 2618 | 7346 | 24687 |
| Neo4j      | 2513 | 6126 | 10902 |
| PathFinder | 2247 | 3981 | 5907 |
