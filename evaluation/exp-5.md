# Exp-5: Planning Latency

## Plan Generation Latency on FinBench & SO (ms)

|  | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P3   | 3.042 | 3.811 | 2.842 | 3.489 | 3.356 | 4.128 | 3.574 | 3.917 |
| GU   | 2.717 | 3.506 | 2.545 | 3.39  | 2.983 | 3.762 | 3.185 | 3.521 |
| Neo4j | 14.1 | 8.2 | 6.7 | 5.8 | 15.3 | 9.4 | 7.6 | 6.9 |
| TuGraphDB | 1.21 | 0.98 | 0.96 | 1.36 | 1.35 | 1.12 | 1.08 | 1.43 |


## Plan Generation Latency on WDBench (ms)

|  | TRAIL | ACYCLIC | SIMPLE |
| --- | --- | --- | --- |
| P3   | 2.12 | 2.05 | 2.06 |
| GU   | 1.82 | 1.76 | 1.75 |
| Neo4j | 4.6 | 6.1 | 6.3 |
| Kuzu | 0.81 | 0.78 | 0.83 |
| PathFinder | 0.34 | 0.31 | 0.35 |

## Plan Generation Latency on Pokec (ms)

|  | TRAIL | ACYCLIC | SIMPLE |
| --- | --- | --- | --- |
| P3   | 2.15 | 1.97 | 2.11 |
| GU   | 1.84 | 1.69 | 1.81 |
| Neo4j | 4.8 | 5.9 | 6.1 |
| Kuzu | 0.84 | 0.76 | 0.85 |
| PathFinder | 0.32 | 0.33 | 0.36 |
