# FinBench Dataset

## Overview

FinBench is an LDBC benchmark for financial graph analysis. This directory contains scripts for downloading, preparing, and converting the dataset.

## Step 1: Download

Use `prepare_datasets.sh` to download and extract the dataset:

```bash
bash prepare_datasets.sh
```

This downloads SF1 and SF10 (with parameters) from the TuGraph OSS mirror, verifies MD5 checksums, and extracts the archives.

For other scale factors, download manually from the links in the parent [README](../README.md).

## Step 2: Convert Timestamps

Run `convert_data.sh` to convert temporal data to the required format:

```bash
bash convert_data.sh sf10    # replace with desired scale factor
```

This backs up the original `snapshot/` directory to `snapshot.bak/` and writes the converted data to a new `snapshot/`.

## Parameter Files

`SF10-params/` contains the original parameter files (`Q1.csv`–`Q4.csv`) from the FinBench SF10 dataset generator. Format: pipe-delimited, columns `id|startTime|endTime|truncationLimit|truncationOrder`.
