# Kuzu Setup and Benchmarking

## Overview

This directory contains setup scripts and benchmarking code for evaluating Kuzu on path query workloads.

The testing workflow uses the Pokec dataset as an example. Other datasets follow a similar procedure.

## Docker Setup

Start a Kuzu environment using Docker:

```bash
docker pull python:3.10
docker run -d --name kuzu-py --privileged -v "/data:/workspace/data" -w /workspace python:3.10 tail -f /dev/null
```

### Install Kuzu

```bash
docker exec -it kuzu-py bash
pip3 install kuzu
```

## Data Import

Run the import script to load datasets:

```bash
./start.sh
```

## Running Benchmarks

Execute benchmark scripts for different query types:

```bash
docker exec -it kuzu-py /bin/bash

python bench/query-acyclic.py
python bench/query-trail.py
python bench/query-simple.py
```

Each script evaluates query performance with specific path mode constraints.

## Configuration

Kuzu (v0.11.3) is an embedded database with no standalone server process and no separate configuration file. All parameters were left at their defaults for a fair out-of-the-box comparison.

- **Buffer pool size**: default (automatically sized to available system memory)
- **Threads**: default (uses all available CPU cores)
- **Query timeout**: not set
- **Index**: primary key index auto-created; no additional indexes
