#!/usr/bin/env python3
"""Generate random parameter files for Pokec queries.

Usage:
    python3 gen_params.py [count] [max_value]

Defaults: count=120, max_value=1000
"""

import random
import sys


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    max_value = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

    random.seed(42)
    for _ in range(count):
        print(random.randint(1, max_value))


if __name__ == "__main__":
    main()
