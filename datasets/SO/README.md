# Stack Overflow Dataset

## Overview

Stack Overflow is a temporal interaction network extracted from user activities on Stack Overflow, sourced from the KONECT collection.

## Download

```bash
wget http://konect.cc/files/download.tsv.stackexchange-stackoverflow.tar.bz2
tar -xjf download.tsv.stackexchange-stackoverflow.tar.bz2
```
The extracted file `out.stackexchange-stackoverflow` contains edges in the format:
```
awk '
BEGIN{
    print "id" > "nodes.csv";
    print "start,end,ts" > "edges.csv";
}
!/^%/ {
    print $1 "," $2 "," $4 >> "edges.csv";
    nodes[$1]=1;
    nodes[$2]=1;
}
END{
    for (n in nodes) print n >> "nodes.csv";
}
' out.stackexchange-stackoverflow
```

### Temporal Interval Generation

The original dataset contains only single timestamps. To generate temporal intervals for path queries, we follow the methodology from the paper *"Efficiently Answering Reachability and Path Queries on Temporal Bipartite Graphs"*:

- **Starting Time**: Use the original timestamp as the edge starting time
- **Duration**: Generate edge duration (1-48 hours) following a power-law distribution with α = -2.5
- **Ending Time**: Computed as starting time + duration

This is implemented in the script `gen_interval_edges.py`. Run the script as follows:

```bash
python gen_interval_edges.py out.stackexchange-stackoverflow edges_interval.csv
```

This approach simulates realistic temporal durations commonly observed in real-world temporal networks.

## Reference

KONECT Network Collection: http://konect.cc/
