# TuGraphDB Setup and Benchmarking

## Overview

This directory contains setup instructions and configuration files for evaluating TuGraphDB on FinBench and SO datasets.

## Prerequisites

Pull the TuGraph Docker image:

```bash
docker pull tugraph/tugraph-runtime-centos7
```

Reference: [TuGraphDB Quick Start Guide](https://github.com/TuGraph-family/tugraph-db/blob/master/docs/zh-CN/source/3.quick-start/1.preparation.md)

## Docker Container Setup

Start the TuGraph container with mounted data and log directories:

**Note**: Replace `/data/dataset` and `/data/log` with your actual directory paths.

```bash
docker run -dt -p 7070:7070 -p 7687:7687 -p 9090:9090 \
    -v /data/dataset:/var/lib/lgraph/data \
    -v /data/log:/var/log/lgraph_log \
    --name tugraph_finbench \
    tugraph/tugraph-runtime-centos7:latest \
    /bin/bash
```

Enter the container:

```bash
docker exec -it tugraph_finbench bash
```

## Data Import

Reference: [TuGraphDB Data Import Guide](https://github.com/TuGraph-family/tugraph-db/blob/master/docs/zh-CN/source/6.utility-tools/1.data-import.md)

### Import Configuration

The import configuration file `import.config` is provided in this directory. Place it in your dataset directory before importing.

### Import Commands

Navigate to the snapshot directory of your dataset and run the import command:

```bash
# For SF 0.1
cd /var/lib/lgraph/data/sf0.1/snapshot
lgraph_import -c /var/lib/lgraph/data/import.config --dir /data/lgraph_db \
    --graph tugraph_finbench --overwrite true --delimiter "|" --v3 0

# For SF 1
cd /var/lib/lgraph/data/sf1/snapshot
lgraph_import -c /var/lib/lgraph/data/import.config --dir /data/lgraph_db \
    --graph tugraph_sf1 --overwrite true --delimiter "|" --v3 0

# For SF 10
cd /var/lib/lgraph/data/sf10/snapshot
lgraph_import -c /var/lib/lgraph/data/import.config --dir /data/lgraph_db \
    --graph tugraph_sf10 --overwrite true --delimiter "|" --v3 0

# For SF 30
cd /var/lib/lgraph/data/sf30/snapshot
lgraph_import -c /var/lib/lgraph/data/import.config --dir /data/lgraph_db \
    --graph tugraph_sf30 --overwrite true --delimiter "|" --v3 0

# For SF 100
cd /var/lib/lgraph/data/sf100/snapshot
lgraph_import -c /var/lib/lgraph/data/import.config --dir /data/lgraph_db \
    --graph tugraph_sf100 --overwrite true --delimiter "|" --v3 0
```

## Running TuGraph Server

Start the TuGraph server inside the container:

```bash
# Stop any running instance
lgraph_server -d stop

# Start server for different scale factors
lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sf01 -d start
lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sf1 -d start
lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sf10 -d start
lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sf30 -d start
lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sf100 -d start
```

**Note**: Update the log directory path when switching between different scale factors.

## Client Access

### Command Line Interface

Reference: [TuGraph Bolt Console Client](https://github.com/TuGraph-family/tugraph-db/blob/master/docs/zh-CN/source/7.client-tools/6.bolt-console-client.md)

Connect to TuGraph using the CLI:

```bash
# Default database
lgraph_cli --ip 127.0.0.1 --port 7687 --graph default \
    --user admin --password 73@TuGraph

# Connect to specific scale factor databases
lgraph_cli --ip 127.0.0.1 --port 7687 --graph tugraph_sf01 \
    --user admin --password 73@TuGraph
lgraph_cli --ip 127.0.0.1 --port 7687 --graph tugraph_sf1 \
    --user admin --password 73@TuGraph
lgraph_cli --ip 127.0.0.1 --port 7687 --graph tugraph_sf10 \
    --user admin --password 73@TuGraph
lgraph_cli --ip 127.0.0.1 --port 7687 --graph tugraph_sf30 \
    --user admin --password 73@TuGraph
lgraph_cli --ip 127.0.0.1 --port 7687 --graph tugraph_sf100 \
    --user admin --password 73@TuGraph
```

### Python Client

Reference: [TuGraph Python Client](https://github.com/TuGraph-family/tugraph-db/blob/master/docs/zh-CN/source/7.client-tools/1.python-client.md)

Example Python code to connect and query:

```python
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("admin", "73@TuGraph")

with GraphDatabase.driver(URI, auth=AUTH) as client:
    session = client.session(database="tugraph_finbench")
    ret = session.run("MATCH (n:Account) RETURN label(n)")
    for item in ret.data():
        print(item)
```

**Note**: Update the database name in `client.session(database="...")` to match your target database.

Benchmark scripts are located in `/data/tugraph/bench`.

## Container Management

Stop and remove the container:

```bash
docker stop tugraph_finbench
docker rm tugraph_finbench
```

## Files

- `import.config` - Schema and data file configuration for FinBench import
- Benchmark scripts in `/data/tugraph/bench`

## Configuration

TuGraphDB uses `lgraph_server` command-line flags for server configuration. No separate configuration file was used.

**Server** (`tugraph/tugraph-runtime-centos7:latest`):
- **Memory**: no explicit memory configuration; TuGraphDB relies on OS page cache (256 GB host). See [TuGraphDB configuration reference](https://tugraph.tech/docs/tugraph-db/en/4.5.2/installation&running/tugraph-running).
- **Threads**: default (server-side); benchmark driver uses 16 threads
- **Ports**: 7070 (HTTP), 7687 (Bolt), 9090 (RPC)
- **Startup**: `lgraph_server --directory /data/lgraph_db --log_dir /root/lgraph_log_sfXX -d start`
- **Warmup**: `lgraph_warmup -d /data/lgraph_db -g default` before benchmark
- **Client protocol**: Bolt (port 7687, via Python `neo4j` driver)
- **Import**: `lgraph_import` with `import.config` schema, delimiter `|`, `--overwrite true`

## Reference

Official Repository: [TuGraph-DB GitHub](https://github.com/TuGraph-family/tugraph-db)


