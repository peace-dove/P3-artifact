# WDBench Query Templates — PathFinder

### Execute Queries

In another terminal session (use `docker exec` with the container ID):

```bash
cd /workspace/benchmark
python3 run_pathfinder.py wdbench 0 5 bfs
```

Or run directly:
```bash
docker run -it --rm \
    -v /data/PathFinder:/workspace \
    pathfinder-builder \
    bash -c "cd /workspace/benchmark && python3 run_pathfinder.py wdbench 0 5 bfs"
```

## Path Modes

PathFinder supports different path mode constraints:
- `bfs` - Breadth-first search (default)
- `acyclic` - Acyclic paths only
- `simple` - Simple paths only
- `trail` - Trail paths only

Specify the path mode when starting the server with `--path-mode <mode>`.

## Reference

Official Repository: [PathFinder GitHub](https://github.com/AnonCSR/PathFinder)
