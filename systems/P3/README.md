# P3 System

## Overview

P3 is a graph database system evaluated on FinBench, SO, WDBench, and Pokec datasets.

## Prerequisites

- Download the docker image and binary distribution
- Datasets prepared in appropriate format

### Docker Image

Please download from [p3.tar.gz](https://drive.google.com/file/d/1F0f_r_0CWj5lmrlKQvSZceauvFb6vK18/view?usp=drive_link).

Use the following command to load the Docker image:
```bash
gunzip p3.tar.gz
docker load -i p3.tar
```

### Binary Distribution

Please download from [tp_instance_test](https://drive.google.com/file/d/1xzWA9BxWA-PspvkjRSULICTI6Cq5h1zT/view?usp=drive_link).

## Data Import

### FinBench Scale Factors

Data is imported using environment variables `LOAD_DATA=1 LOAD_FIN=1` and persisted in the test directory.

**Import SF0.1:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF01/0
```

**Import SF1:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF1/0
```

**Import SF3:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF3/0
```

**Import SF10:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF10/0
```

**Import SF30:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF30/0
```

**Import SF100:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_FIN=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF100/0
```

### WDBench Import

```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_WD=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0
```

### Pokec Import

```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test && \
LOAD_DATA=1 LOAD_POKEC=1 ./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataPokec/0
```

## Running Benchmarks

### FinBench Queries

Data persists in the import directory. Subsequent queries reference the imported scale factor.

**Query Format:**
```bash
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF{XX}/0:TpInstanceParamTest/TpInstanceTest.{QueryTest}/0
```

**Example - FinBench TCR1 on SF10:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataSF10/0:TpInstanceParamTest/TpInstanceTest.FinTest1BatchId/0
```

**All FinBench Queries (with/without optimization):**
- `FinTest1BatchId` / `FinTest1BatchIdwoopt` - TCR1
- `FinTest2BatchId` / `FinTest2BatchIdwoopt` - TCR2
- `FinTest5BatchId` / `FinTest5BatchIdwoopt` - TCR5
- `FinTest11BatchId` / `FinTest11BatchIdwoopt` - TCR11

### WDBench Path Queries

**ACYCLIC, SIMPLE, TRAIL Path Modes:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test

# ACYCLIC mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeAcyclicTest/0

# SIMPLE mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeSimpleTest/0

# TRAIL mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeTrailTest/0
```

**Different Max Hop Tests:**
```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test

# Max Hop 3
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeMaxHop3Test/0

# Max Hop 4
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeMaxHop4Test/0

# Max Hop 5
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeMaxHop5Test/0

# Max Hop 6
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeMaxHop6Test/0

# Max Hop 7
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataWDBench/0:TpInstanceParamTest/TpInstanceTest.PathModeMaxHop7Test/0
```

### Pokec Queries

```bash
cd /home/{USER}/data_universe/build/output/bin/test/tp_instance_test

# ACYCLIC mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataPokec/0:TpInstanceParamTest/TpInstanceTest.PokecAcyclicTest/0

# SIMPLE mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataPokec/0:TpInstanceParamTest/TpInstanceTest.PokecSimpleTestwoOpt/0

# TRAIL mode
./tp_instance_test \
--gtest_filter=TpInstanceParamTest/TpInstanceTest.ImportDataPokec/0:TpInstanceParamTest/TpInstanceTest.PokecTrailTestwoOpt/0
```

## Building P3

**Compile release version:**
```bash
./build.sh config -type=release -clang
./build.sh compile_target tp_instance_test -j32
```

## Test Suite

The `run.sh` script contains all benchmark commands. Uncomment the desired test and execute:

```bash
bash run.sh
```

## Notes

- Data persistence: Imported data is saved in `/home/{USER}/data_universe/build/output/bin/test/tp_instance_test/`
- All subsequent queries must reference the same directory
- Test names with `woOpt` suffix disable query optimizations
- Use `LOAD_DATA=1` environment variable for initial data import only

## Configuration

P3 is an embedded graph database with no standalone server process and no separate configuration file. Query execution runs as a native binary (`tp_instance_test`) within a Docker container.

- **Memory**: default setting; uses 30% of total system memory (256 GB × 0.3 ≈ 76.8 GB)
- **Threads**: default (internal thread pool)
- **Query timeout**: not set
- **Build type**: Release (`./build.sh config -type=release -clang`)
- **Compilation**: `-j32` parallel build
- **Index**: built automatically during data import; no manual configuration
- **Docker image**: custom (see [p3.tar.gz](https://drive.google.com/file/d/1F0f_r_0CWj5lmrlKQvSZceauvFb6vK18/view?usp=drive_link))

## Reference

See [run.sh](run.sh) for complete command list for additional utilities.
