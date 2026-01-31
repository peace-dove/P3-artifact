# Pokec Dataset

## Overview

Pokec is a social network dataset from SNAP, containing user profiles and friendship relationships.

## Download

```bash
wget https://snap.stanford.edu/data/soc-pokec-profiles.txt.gz
wget https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz
gunzip soc-pokec-profiles.txt.gz
gunzip soc-pokec-relationships.txt.gz
```

## Data Extraction

Extract the first three columns from both vertex and edge files using shell scripts, as only these columns are needed for path query evaluation.
