# P^3: Enabling On-the-fly Filtering for Prefix-Rejecting Path Predicates

This repository contains implementations and experimental evaluation for **"P^3: Enabling On-the-fly Filtering for Prefix-Rejecting Path Predicates"** across multiple graph database systems.

## Directory Structure

```
├── datasets/       # Benchmark datasets (FinBench, SO, WDBench, Pokec)
├── queries/        # Query templates and parameters
├── evaluation/     # Experimental results (Exp-1 ~ Exp-7)
└── systems/        # Graph database systems (Kuzu, Neo4j, P3, PathFinder, TuGraphDB)
```

## Quick Start

### 1. Datasets

**Available Datasets**:
- **FinBench**: Financial transaction networks (1.1M vertices, 10.4M edges at SF10)
- **Stack Overflow**: Temporal interaction network (642K vertices, 1.3M edges)
- **Wikidata**: Knowledge graph (364M vertices, 1.26B edges)
- **Pokec**: Social network (1.63M vertices, 30.6M edges)

See [datasets/README.md](datasets/README.md) for details.

### 2. Systems Setup

Each system directory contains setup and benchmarking scripts:

- **[Kuzu](systems/Kuzu/)**: Embedded Cypher database
- **[Neo4j](systems/Neo4j/)**: Graph database (`neo4j:2026.03.1`)
- **[P3](systems/P3/)**: Our system with prefix-rejecting predicates processing
- **[GU](systems/GU/)**: Native graph database (baseline without PRP optimization)
- **[PathFinder](systems/PathFinder/)**: Path-optimized system
- **[TuGraphDB](systems/TuGraphDB/)**: High-performance graph database

Each system README includes:
- Installation and configuration
- Data import procedures
- Query execution examples
- Benchmark scripts

See [systems/README.md](systems/README.md) for overview.

### 3. Running Queries

Query execution is system-specific:

```bash
# Query definitions and parameters
cd queries

# For each system, refer to queries/{Dataset}/{System}/README.md
# Example: queries/WDBench/PathFinder/README.md
```

See [queries/README.md](queries/README.md) for structure.

### 4. Results

Experimental results are organized as seven reports in `evaluation/`:

- **Exp-1** — Performance Improvement
- **Exp-2** — Pruning Effect
- **Exp-3** — Memory Usage
- **Exp-4** — State Compression
- **Exp-5** — Planning Latency
- **Exp-6** — Scalability
- **Exp-7** — Case Study

See [evaluation/README.md](evaluation/README.md) for an overview of each experiment.

## License

Apache License 2.0 - See LICENSE file for details.
