#!/usr/bin/env python3
"""Generate random parameter files for Stack Overflow queries.

Generates:
  - Q5-single.txt / Q7-single.txt: 120 random single-source IDs (1..10000)
  - Q6-pair.txt   / Q8-pair.txt:   120 random source-target pairs (1..10000)

Usage:
    python3 gen_params.py [count] [max_value]

Defaults: count=120, max_value=10000
"""

import random
import sys
import os


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    max_value = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    random.seed(42)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for name in ["Q5-single.txt", "Q7-single.txt"]:
        with open(os.path.join(script_dir, name), "w") as f:
            for _ in range(count):
                f.write(f"{random.randint(1, max_value)}\n")

    for name in ["Q6-pair.txt", "Q8-pair.txt"]:
        with open(os.path.join(script_dir, name), "w") as f:
            for _ in range(count):
                src = random.randint(1, max_value)
                dst = random.randint(1, max_value)
                while dst == src:
                    dst = random.randint(1, max_value)
                f.write(f"{src} {dst}\n")


if __name__ == "__main__":
    main()
