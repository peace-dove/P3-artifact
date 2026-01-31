# Exp-4: State Compression

## Execution time on FinBench & SO (ms)

| | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GU   | 2181.61 | 2691.12 | 2429.48 | 1190.64 | 5634 | 5177 | 7539 | 7264 |
| P3-noSC | 1635 | 2176 | 1873 | 697 | 4348 | 4124 | 6023 | 5795 |
| P3      | 1536.69 | 1860.42 | 1705.62 | 669.76 | 3935 | 3768 | 5734 | 5554 |

> Remark: Q4 already benefits from aggressive pruning with few surviving paths, while Q7–Q8 involve only a single sliding window check, leaving little room for further optimization.

## Execution time on WDBench (ms)

| | TRAIL | ACYCLIC | SIMPLE |
| --- | --- | --- | --- |
| GU   | 261.76 | 264.33 | 263.37 |
| P3-noSC | 151.75 | 128.48 | 143.62 |
| P3      | 132.85 | 107.38 | 122.81 |

## Memory on WDBench (MB)

Setup: WDBench, hop 1–5.

> Remark: Base memory overhead is about 3571 MB, which has been subtracted from all values below. The numbers reflect query-execution-only memory consumption.

| | TRAIL | ACYCLIC | SIMPLE |
| --- | --- | --- | --- |
| GU   | 3653 | 3321 | 3464 |
| P3-noSC | 2620 | 2262 | 2391 |
| P3      | 1926 | 1607 | 1770 |
