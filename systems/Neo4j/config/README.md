# Neo4j Configuration Tuning

Three memory configurations tested on a 256 GB machine. Performance difference across all three is within 5%. The paper uses `neo4j.1.conf`.

## Execution Time Comparison

Average execution time per query (ms). FinBench averages over Q1–Q4; SO averages over Q5–Q8; WDBench and Pokec average over TRAIL/ACYCLIC/SIMPLE.

| Config | FinBench (ms) | SO (ms) | WDBench (ms) | Pokec (ms) |
|--------|--------------|---------|-------------|------------|
| `neo4j.1.conf` (used in paper) | 2686 | 31722 | 3283 | 8596 |
| `neo4j.2.conf` | 2714 | 31958 | 3391 | 8703 |
| No custom config | 2798 | 32513 | 3342 | 8935 |

Max deviation: FinBench 4.2%, SO 2.5%, WDBench 3.3%, Pokec 3.9%.

See [evaluation/exp-1.md](../../../evaluation/exp-1.md) for the full per-query breakdown.
