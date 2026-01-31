# Experimental Results

This directory contains the experimental results reported in our evaluation of P3 on FinBench, SO, WDBench, and Pokec.

## Contents

- [`exp-1.md`](exp-1.md) — **Performance Improvement.** End-to-end query latency of P3 and GU against Neo4j, TuGraphDB, Kuzu, and PathFinder on FinBench (Q1–Q4), SO (Q5–Q8), WDBench, and Pokec.

- [`exp-2.md`](exp-2.md) — **Pruning Effect.** Surviving-path counts before/after PRP-based pruning at each hop, plus per-hop reduction ratios on FinBench, SO, WDBench, and Pokec.

- [`exp-3.md`](exp-3.md) — **Memory Usage.** Query-execution memory consumption of P3, GU, Neo4j, Kuzu, and PathFinder on Pokec (aggregate across hop 3–7, and by hop length).

- [`exp-4.md`](exp-4.md) — **State Compression.** Comparison of P3 (full), P3-noSC (state-cache disabled), and GU in execution time on FinBench/SO/WDBench and memory on WDBench.

- [`exp-5.md`](exp-5.md) — **Planning Latency.** Plan generation latency of P3, GU, Neo4j, TuGraphDB, Kuzu, and PathFinder on FinBench/SO, WDBench, and Pokec.

- [`exp-6.md`](exp-6.md) — **Scalability.** P3 vs. GU latency on FinBench Q1–Q4 across scale factors SF=1/3/10/30/100, and throughput (QPS) of P3, GU, Neo4j, TuGraphDB at 2/4/8/16/32 threads.

- [`exp-7.md`](exp-7.md) — **Case Study.** Per-loop surviving-path counts on two representative queries (FinBench TCR1 at 1–5 hop; WDBench ACYCLIC at 3–7 hop from a single source).
