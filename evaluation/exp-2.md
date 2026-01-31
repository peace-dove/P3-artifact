# Exp-2: Pruning Effect

## FinBench

|  | Hop 2 (before) | Hop 2 (after) | Hop 2 (reduction) | Hop 3 (before) | Hop 3 (after) | Hop 3 (reduction) |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | 21805 | 13597 | 37.64% | 44561 | 19673 | 60.80% |
| Q2 | 34294 | 21602 | 37.01% | 86236 | 36564 | 57.60% |
| Q3 | 34661 | 22069 | 36.33% | 83124 | 32668 | 60.78% |
| Q4 | 1122 | 81 | 92.54% | 1126 | 84 | 92.40% |

## SO

|  | Hop 2 (before) | Hop 2 (after) | Hop 2 (reduction) | Hop 3 (before) | Hop 3 (after) | Hop 3 (reduction) | Hop 4 (before) | Hop 4 (after) | Hop 4 (reduction) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q5 | 69325 | 64279 | 7.28% | 92727 | 76371 | 17.64% | 212425 | 163992 | 22.80% |
| Q6 | 69325 | 64279 | 7.28% | 92727 | 76955 | 17.01% | 196086 | 153731 | 21.60% |
| Q7 | 83217 | 73847 | 11.26% | 120563 | 91025 | 24.50% | - | - | - |
| Q8 | 83217 | 73847 | 11.26% | 113769 | 84644 | 25.60% | - | - | - |

> Remark: For time-interval reachability queries, the predicate uses a 2-hop sliding window over consecutive edges. Q5/Q6 share the same source vertex (identical Hop 2 counts); so do Q7/Q8.

## WDBench

|  | Hop 2 (before / after / reduction) | Hop 3 (before / after / reduction) | Hop 4 (before / after / reduction) | Hop 5 (before / after / reduction) | Avg reduction |
| --- | --- | --- | --- | --- | --- |
| TRAIL | 509 / 356 / 30.06% | 728 / 455 / 37.50% | 960 / 538 / 43.96% | 1269 / 658 / 48.15% | 39.92% |
| ACYCLIC | 463 / 287 / 38.01% | 662 / 357 / 46.07% | 873 / 418 / 52.12% | 1154 / 490 / 57.54% | 48.44% |
| SIMPLE | 486 / 330 / 32.10% | 696 / 411 / 40.95% | 917 / 486 / 47.00% | 1212 / 588 / 51.49% | 42.88% |

## Pokec

|  | Hop 3 (before / after / reduction) | Hop 4 (before / after / reduction) | Hop 5 (before / after / reduction) | Hop 6 (before / after / reduction) | Hop 7 (before / after / reduction) |
| --- | --- | --- | --- | --- | --- |
| TRAIL | 667 / 562 / 15.74% | 1866 / 1534 / 17.79% | 5122 / 4143 / 19.11% | 9379 / 7178 / 23.47% | 25651 / 17609 / 31.35% |
| ACYCLIC | 603 / 466 / 22.72% | 1687 / 1269 / 24.78% | 4631 / 3421 / 26.13% | 8479 / 5895 / 30.48% | 23190 / 14065 / 39.35% |
| SIMPLE | 641 / 527 / 17.79% | 1793 / 1438 / 19.80% | 4923 / 3883 / 21.13% | 9013 / 6716 / 25.49% | 24651 / 16430 / 33.35% |
| Avg reduction | 18.75% | 20.79% | 22.12% | 26.48% | 34.68% |
