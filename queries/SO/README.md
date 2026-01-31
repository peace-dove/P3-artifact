# Stack Overflow Queries

## Overview

This directory contains query templates for evaluating temporal path queries on the Stack Overflow dataset. All queries match alternating `P2L`/`L2P` edge patterns (User → Location → User → …) with temporal constraints.

Query parameters (IDs) are randomly sampled from entities in the dataset at runtime.

## Query Summary

| Query | Type | Temporal Constraint | Source / Target |
|-------|------|---------------------|-----------------|
| Q5 | Timestamp ordering | `max(ts)` of V-pair ≤ `min(ts)` of next V-pair | Single-source |
| Q6 | Timestamp ordering | Same as Q5 | Point-to-point |
| Q7 | Interval overlap + sequential | `max(s1,s2) < min(e1,e2)` within V-pair; `prev.e ≤ next.s` across V-pairs | Single-source |
| Q8 | Interval overlap + sequential | Same as Q7 | Point-to-point |

## Parameters

`params/` contains 120 randomly generated test inputs per query (IDs in range 1–10000):

| File | Format |
|------|--------|
| `Q5-single.txt` / `Q7-single.txt` | One source ID per line |
| `Q6-pair.txt` / `Q8-pair.txt` | `src dst` pair per line |

Regenerate with `python3 params/gen_params.py [count] [max_value]` (defaults: 120, 10000).

## Implementations

| Directory | Language | Key Features |
|-----------|----------|--------------|
| [Neo4j](Neo4j/) | Cypher 25 | QPP + `allReduce()` for early pruning |
| [P3](P3/) | GQL | Sliding window (`SW`) for declarative temporal constraints |
| [GU](GU/) | GQL | UDFs (`isAsc`, `isAscInterval`) for temporal constraints (no SW) |
| [TuGraphDB](TuGraphDB/) | Cypher | `isAsc(getMemberProp(...))` helper functions (Q5/Q6 only) |
