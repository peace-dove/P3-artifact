# WDBench Queries

## Overview

This directory contains query templates for evaluating path mode constraints (TRAIL, ACYCLIC, SIMPLE) on the WDBench (Wikidata) dataset.

## Query Selection

The original WDBench benchmark provides 639 Cypher query templates (`params/origin_query.cypher`). We select 80 single-edge-type reachability queries whose structure is compatible with path mode evaluation, and use their start node IDs as parameters (`params/params-pathmodes.txt`, 80 unique IDs repeated for 2 rounds = 160 lines).

## Query Generation

`change.py` converts Cypher templates to GQL syntax (Entity → WDEntity, edge types → `WDRel` with `prop` filter, hop ranges → GQL quantifier syntax).

## Implementations

| Directory | Language | Path Mode Strategy |
|-----------|----------|--------------------|
| [Neo4j](Neo4j/) | Cypher 25 | TRAIL by default; ACYCLIC/SIMPLE via `allReduce()` |
| [P3](P3/) | GQL | `TRAIL`/`ACYCLIC`/`SIMPLE` keywords in MATCH clause |
| [GU](GU/) | GQL | Same as P3 (identical query statements) |
| [Kuzu](Kuzu/) | Cypher | `is_trail()`/`is_acyclic()` built-ins; SIMPLE via `ACYCLIC` + `list_slice` |
| [PathFinder](PathFinder/) | Custom | `--path-mode` flag at server startup |
