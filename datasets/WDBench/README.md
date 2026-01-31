# WDBench Dataset

## Overview

WDBench is a large-scale Wikidata benchmark for evaluating property path queries on knowledge graphs.

## Setup Instructions

Follow the dataset preparation workflow from the official [WDBench repository](https://github.com/MillenniumDB/WDBench).

Specifically, replicate the Neo4j data loading process as described in their documentation.

## Data Processing

This directory contains helper scripts for converting the dataset:
- `filter_direct_properties.py` - Filters direct property relationships
- `nt_to_neo4j.py` - Converts N-Triples format to Neo4j import format. Use the script `nt_to_neo4j.py` to generate the .csv files `entities.csv`, `literals.csv` and `edges.csv`.
