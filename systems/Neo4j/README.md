# Neo4j Setup and Benchmarking

## Docker Image

```bash
docker pull neo4j:2026.03.1
```

## Overview

This directory contains setup scripts and benchmarking code for evaluating Neo4j on FinBench, SO, WDBench, and Pokec datasets.

## Prerequisites

- Docker with Neo4j image (`neo4j:2026.03.1`)
- Python 3 with neo4j driver
- Dataset files prepared in CSV format

> **Note**: The `myclear-pokec.sh`, `myload-pokec.sh`, and `mystart.sh` scripts use Pokec as the active example (simplest pipeline). Commands for other datasets (FinBench, WDBench, SO) are commented out in each script for reference.

## Data Preparation

### 1. Clear Import Directory

**Warning**: Execute clear scripts carefully. Verify the target directory before running.

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo
bash myclear.sh
```

For Pokec dataset:
```bash
bash myclear-pokec.sh
```

### 2. Convert Data Format

Run conversion scripts to transform timestamps:

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import
rm -f *.csv
```

### 3. Copy Dataset Files

Copy dataset files to the import directory:

```bash
# Navigate to dataset directory (choose appropriate scale factor)
cd /data/dataset/sf0.1/snapshot    # or sf1, sf10, sf100

# Copy required CSV files
cp \
  Account.csv \
  Loan.csv \
  Medium.csv \
  Person.csv \
  AccountTransferAccount.csv \
  MediumSignInAccount.csv \
  PersonOwnAccount.csv \
  LoanDepositAccount.csv \
  PersonGuaranteePerson.csv \
  PersonApplyLoan.csv \
  /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import/
```

### 4. Convert CSV Headers

Convert CSV headers to Neo4j format:

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/bench
python3 convert_csv_header.py
```

### 5. Copy Parameter Files

Place parameter files in the benchmark directory:

```bash
# Navigate to parameter directory (choose appropriate scale factor)
cd /data/dataset/sf1/params    # or sf10, sf100

# Copy parameter files
cp complex_1_param.csv complex_2_param.csv complex_5_param.csv complex_11_param.csv \
   /data/ldbc_finbench_transaction_impls/neo4j/neo/bench/params_sf1/
```

## Data Import

### FinBench Dataset

Run the import script:

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/
bash myload.sh
```

Or import manually:

```bash
# Stop existing container
docker stop finbench-neo4j

# Clear data directory
rm -rf /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data/*

# Import data
docker run \
    --rm \
    --publish=7474:7474 \
    --publish=7687:7687 \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/import:z \
    neo4j:2026.03.1 \
    neo4j-admin database import full \
    --nodes=Account="/import/Account.csv" \
    --nodes=Loan="/import/Loan.csv" \
    --nodes=Medium="/import/Medium.csv" \
    --nodes=Person="/import/Person.csv" \
    --relationships=ACCOUNT_TRANSFER_ACCOUNT="/import/AccountTransferAccount.csv" \
    --relationships=MEDIUM_SIGNIN_ACCOUNT="/import/MediumSignInAccount.csv" \
    --relationships=PERSON_OWN_ACCOUNT="/import/PersonOwnAccount.csv" \
    --relationships=LOAN_DEPOSIT_ACCOUNT="/import/LoanDepositAccount.csv" \
    --relationships=PERSON_GUARANTEE_PERSON="/import/PersonGuaranteePerson.csv" \
    --relationships=PERSON_APPLY_LOAN="/import/PersonApplyLoan.csv" \
    --delimiter '|'
```

### Pokec Dataset

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/
bash myload-pokec.sh
```

## Memory Configuration

### Using `neo4j-admin server memory-recommendation`

Neo4j provides a built-in tool to recommend memory settings based on the current database size and available system resources. Run it inside the container after data import:

```bash
docker exec -it <container-name> neo4j-admin server memory-recommendation
```

Output on our 247.8GB machine (Pokec dataset, ~1200MB data + native indexes, no Lucene indexes):

```
# Assuming the system is dedicated to running Neo4j and has 247.8GiB of memory,
# we recommend a heap size of around 31g, and a page cache of around 197g,
# and that about 20200m is left for the operating system, and the native memory
# needed by Lucene and Netty.
#
# Tip: If the indexing storage use is high, e.g. there are many indexes or most
# data indexed, then it might advantageous to leave more memory for the
# operating system.
#
# Tip: The more concurrent transactions your workload has and the more updates
# they do, the more heap memory you will need. However, don't allocate more
# than 31g of heap, since this will disable pointer compression, also known as
# "compressed oops", in the JVM and make less effective use of the heap.
#
# Tip: Setting the initial and the max heap size to the same value means the
# JVM will never need to change the heap size. Changing the heap size otherwise
# involves a full GC, which is desirable to avoid.
#
# Based on the above, the following memory settings are recommended:
server.memory.heap.initial_size=31g
server.memory.heap.max_size=31g
server.memory.pagecache.size=197g
#
# It is also recommended turning out-of-memory errors into full crashes,
# instead of allowing a partially crashed database to continue running:
server.jvm.additional=-XX:+ExitOnOutOfMemoryError
#
# Total size of lucene indexes in all databases: 0k
# Total size of data and native indexes in all databases: 1200m
```

Docs: https://neo4j.com/docs/operations-manual/current/configuration/neo4j-admin-memrec/

### Configuration Tuning Experiments

We tested three configurations on our 256 GB machine. The performance difference across all three was within 5%. The paper uses `neo4j.1.conf` (best overall). Note that the observed memory usage scales proportionally with the configured heap and page cache sizes.

| Config | Heap | PageCache | Source |
|--------|------|-----------|--------|
| No custom config | container default | container default | Neo4j built-in defaults |
| `config/neo4j.1.conf` | 16g | 160g | Refer to [ldbc_finbench_transaction_impls](https://github.com/ldbc/ldbc_finbench_transaction_impls) |
| `config/neo4j.2.conf` | 31g | 197g | Generated by `neo4j-admin server memory-recommendation` |

To use a specific config, copy it before starting:

```bash
# Use config 1 (used in paper)
cp config/neo4j.1.conf /data/ldbc_finbench_transaction_impls/neo4j/conf/neo4j.conf

# Or use config 2
cp config/neo4j.2.conf /data/ldbc_finbench_transaction_impls/neo4j/conf/neo4j.conf

# Then start (mounts conf/ into the container)
bash mystart.sh
```

For the default (no custom config) experiment, start without mounting the `conf/` volume.

For a comparison of execution times across different configurations, see [config/README.md](config/README.md).

## Starting Neo4j Server

Use the startup script:

```bash
bash mystart.sh
```

## Running Benchmarks

Execute benchmark Python scripts:

```bash
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/bench
python3 bench_xx.py
```

### Running in Background

To run benchmarks in the background with output redirection:

```bash
nohup python3 -u bench1.py > log/1.log 2>&1 &
```

**Note**: The `-u` flag forces unbuffered output, ensuring logs are written immediately.

## Using Cypher Shell

Enter the container:

```bash
docker exec -it finbench-neo4j cypher-shell
```

## Reference

- [Neo4j CSV Import Guide](https://medium.com/@matthewghannoum/import-your-csv-data-into-a-neo4j-graph-database-d019b95115b1)
- [Neo4j Admin Import Documentation](https://neo4j.com/docs/operations-manual/current/tutorial/neo4j-admin-import/#_id_space)
- [Neo4j Memory Recommendation](https://neo4j.com/docs/operations-manual/current/configuration/neo4j-admin-memrec/)
