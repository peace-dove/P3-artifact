# Pokec Queries

Path query templates on the Pokec social network dataset, covering three path semantics: acyclic, simple, and trail.

## Directory Structure

| Directory | Description |
|-----------|-------------|
| [P3](P3/) | GQL with `ACYCLIC`/`SIMPLE`/`TRAIL` keywords in MATCH clause |
| [GU](GU/) | GQL — same as P3 (identical query statements) |
| [Kuzu](Kuzu/) | Cypher with Kuzu predicate functions (`is_acyclic`, `is_trail`) and inline path modes |
| [Neo4j](Neo4j/) | Cypher with manual path constraint implementation via `REDUCE`/`ALL` |
| [PathFinder](PathFinder/) | PathFinder execution instructions |
| [params](params/) | Parameter files (120 random user IDs each) and generation script |

## Parameter Files

| File | Usage |
|------|-------|
| `params/params-acyclic.txt` | Parameters for acyclic queries |
| `params/params-simple.txt` | Parameters for simple queries |
| `params/params-trail.txt` | Parameters for trail queries |
| `params/gen_params.py` | Random parameter generator (`python3 gen_params.py [count] [max_value]`, defaults: 120, 1000) |
