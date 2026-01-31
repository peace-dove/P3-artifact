# GU (Baseline)

GU is a native graph database used as the baseline in our experiments. It shares the same binary, Docker image, and data import process as P3, but runs without PRP optimization.

To run GU queries, use the test names with the `woOpt` suffix (e.g., `FinTest1BatchIdwoopt` instead of `FinTest1BatchId`).

See [P3 README](../P3/README.md) for setup, data import, and benchmark instructions.
