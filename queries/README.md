# Queries

This directory contains query templates and parameters for all benchmark datasets.

## Datasets

| Dataset | Queries | Focus | Systems |
|---------|---------|-------|---------|
| [FinBench](FinBench/) | Q1–Q4 | Temporal path constraints (transfer chains, guarantees) | Neo4j, P3, GU, TuGraphDB |
| [Pokec](Pokec/) | TRAIL / ACYCLIC / SIMPLE | Path mode semantics on social network | Neo4j, P3, Kuzu, GU, PathFinder |
| [SO](SO/) | Q5–Q8 | Temporal V-pattern constraints (timestamp ordering, interval overlap) | Neo4j, P3, GU, TuGraphDB |
| [WDBench](WDBench/) | TRAIL / ACYCLIC / SIMPLE | Path mode semantics on Wikidata knowledge graph (80 queries from WDBench) | Neo4j, P3, GU, Kuzu, PathFinder |

## Query Templates

All queries are **parameterized templates** — node IDs, timestamps, and other parameters are substituted at runtime from parameter files in each dataset's `params/` directory.
