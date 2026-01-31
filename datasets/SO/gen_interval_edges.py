import numpy as np
import sys

ALPHA = 2.5              # power-law exponent
MIN_DURATION = 3600      # 1 hour (seconds)
MAX_DURATION = 48 * 3600 # 48 hours (seconds)
SEED = 42

def sample_power_law(size):
    rng = np.random.default_rng(SEED)
    r = rng.random(size)

    a = MIN_DURATION
    b = MAX_DURATION
    alpha = ALPHA

    # truncated power-law inverse CDF
    x = ( (b**(1-alpha) - a**(1-alpha)) * r + a**(1-alpha) ) ** (1/(1-alpha))
    return x.astype(int)

def main(input_file, output_file):

    edges = []

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("%"):
                continue

            parts = line.strip().split()
            if len(parts) < 4:
                continue

            start = parts[0]
            end = parts[1]
            ts = int(parts[3])

            edges.append((start, end, ts))

    n = len(edges)
    durations = sample_power_law(n)

    with open(output_file, "w") as out:
        out.write("start,end,s,e\n")

        for i, (start, end, ts) in enumerate(edges):
            s = ts
            e = ts + int(durations[i])
            out.write(f"{start},{end},{s},{e}\n")

    print(f"Generated {n} interval edges -> {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gen_interval_edges.py input_file output_file")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
