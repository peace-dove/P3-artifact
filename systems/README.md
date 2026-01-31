# Systems

Setup and benchmarking scripts for each graph database system evaluated in this project.

| System | Deployment | Datasets |
|--------|------------|----------|
| [Neo4j](Neo4j/) | Docker (`neo4j:2026.03.1`) | FinBench, SO, WDBench, Pokec |
| [P3](P3/) | Docker + native binary | FinBench, SO, WDBench, Pokec |
| [GU](GU/) | Docker + native binary | FinBench, SO, WDBench, Pokec |
| [TuGraphDB](TuGraphDB/) | Docker (`tugraph-runtime-centos7`) | FinBench, SO |
| [Kuzu](Kuzu/) | Docker (`python:3.10` + pip) | Pokec, WDBench |
| [PathFinder](PathFinder/) | Docker (`ubuntu:20.04`, build from source) | Pokec, WDBench |

Each subdirectory contains a README with data import, server startup, and benchmark execution instructions.
