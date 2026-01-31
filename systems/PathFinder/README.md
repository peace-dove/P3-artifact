# PathFinder Setup and Benchmarking

## Overview

This directory contains setup instructions and benchmarking scripts for evaluating PathFinder on path query workloads.

PathFinder requires Ubuntu 20.04 and specific dependencies. We use Docker for consistent build environments.

## Prerequisites

### Docker Image

Create a Docker image with required dependencies:

```dockerfile
FROM ubuntu:20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# Install dependencies
RUN apt-get update && apt-get install -y \
    git g++ cmake libssl-dev libncurses-dev locales less wget \
    python3 python3-pip sudo lsof \
    && rm -rf /var/lib/apt/lists/*

# Generate locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Set working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
```

Build the image:
```bash
docker build -t pathfinder-builder .
```

## Setup Instructions

### 1. Data Preparation

Follow the data preparation steps from the [PathFinder repository](https://github.com/AnonCSR/PathFinder/blob/main/dbs/README.md#download-and-process-dataset).

### 2. Download Boost Library

Download Boost 1.81.0:
```bash
wget https://archives.boost.io/release/1.81.0/source/boost_1_81_0.tar.gz
```

For detailed setup instructions, refer to the [PathFinder setup guide](https://github.com/AnonCSR/PathFinder/blob/main/pathfinder/README.md).

### 3. Build PathFinder

**Note**: Replace `/data/PathFinder` with your actual PathFinder directory path.

```bash
docker run -it --rm \
    -v /data/PathFinder:/workspace \
    pathfinder-builder \
    bash -c "cd /workspace/pathfinder && \
             cmake -B build/Release -D CMAKE_BUILD_TYPE=Release && \
             cmake --build build/Release/"
```

### 4. Import Data

Import dataset into PathFinder format (example using Pokec):

```bash
docker run --rm \
    -v /data/PathFinder:/workspace \
    pathfinder-builder \
    bash -c "cd /workspace/pathfinder && \
             ./build/Release/bin/pf-import ../dbs/pokec_pathfinder.txt dbs/pokec -m quad"
```

## Running Benchmarks

### Start PathFinder Server

Start the server in interactive mode:

```bash
docker run -it --rm \
    -v /data/PathFinder:/workspace \
    pathfinder-builder \
    /bin/bash
```

Inside the container:
```bash
cd /workspace/pathfinder
./build/Release/bin/pf-server dbs/pokec -t 60 --path-mode bfs
```

**Note**: After starting the interactive container, use `docker ps` to find the container ID, then use `docker exec` to run queries in a separate session.

### Execute Queries

In another terminal session (use `docker exec` with the container ID):

```bash
cd /workspace/benchmark
python3 run_pathfinder.py pokec 0 5 bfs
```

Or run directly:
```bash
docker run -it --rm \
    -v /data/PathFinder:/workspace \
    pathfinder-builder \
    bash -c "cd /workspace/benchmark && python3 run_pathfinder.py pokec 0 5 bfs"
```

## Path Modes

PathFinder supports different path mode constraints:
- `bfs` - Breadth-first search (default)
- `acyclic` - Acyclic paths only
- `simple` - Simple paths only
- `trail` - Trail paths only

Specify the path mode when starting the server with `--path-mode <mode>`.

## Configuration

PathFinder is a research prototype configured entirely through `pf-server` command-line flags. There is no separate configuration file.

- **Memory**: no tuning knob; the database is loaded entirely into memory at startup
- **Threads**: single-threaded query execution; no thread count parameter
- **Query timeout**: `-t 60` (60 seconds per query)
- **Path mode**: `--path-mode <mode>` (set at server startup; requires restart to change)
- **Build type**: Release (`-D CMAKE_BUILD_TYPE=Release`)
- **Index**: built automatically during `pf-import`; no manual configuration

## Reference

Official Repository: [PathFinder GitHub](https://github.com/AnonCSR/PathFinder)
