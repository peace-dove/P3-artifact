#!/usr/bin/env python3
"""Generate 120 batch input parameter sets from Person.csv for Q2, Q3, Q4.

Scans a 60-day window (e.g. 2021-11-01 to 2021-12-30), splitting each day
into 2 half-day slots (00-12, 12-24), producing 60 * 2 = 120 parameter
entries. Each entry contains the person IDs whose createTime falls within
that slot (UTC+8).

Outputs three files with identical structure (same person IDs per slot):
  - Q2_batch_params.csv
  - Q3_batch_params.csv
  - Q4_batch_params.csv

Usage:
    python3 gen_batch_person_params.py [--input sf10/snapshot/Person.csv]
                                       [--start-date 2021-11-01]
                                       [--days 60]
"""

import csv
import argparse
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Generate batch input params from Person.csv")
    parser.add_argument("--input", default="sf10/snapshot/Person.csv",
                        help="Input Person CSV file (pipe-delimited)")
    parser.add_argument("--output-dir", default=".",
                        help="Directory for output files")
    parser.add_argument("--start-date", default="2021-11-01",
                        help="First day of the window (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=60,
                        help="Number of days in the window")
    return parser.parse_args()


def load_persons(input_file):
    """Load all persons with their createTime converted to UTC+8 datetime."""
    persons = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            try:
                ts_ms = int(row["createTime"])
                dt = datetime.utcfromtimestamp(ts_ms / 1000) + timedelta(hours=8)
                persons.append((row, dt))
            except (ValueError, KeyError):
                continue
    return persons


def generate_slots(start_date, num_days):
    """Generate (date_str, start_hour, end_hour) tuples.

    60 days * 2 half-day slots = 120 slots.
    """
    slots = []
    base = datetime.strptime(start_date, "%Y-%m-%d")
    for day_offset in range(num_days):
        current_date = base + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        slots.append((date_str, 0, 12))
        slots.append((date_str, 12, 24))
    return slots


def filter_persons(persons, target_date, start_hour, end_hour):
    """Return person IDs matching the given date and hour range (UTC+8)."""
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    ids = []
    for row, dt in persons:
        if (dt.year == target_dt.year
                and dt.month == target_dt.month
                and dt.day == target_dt.day
                and start_hour <= dt.hour < end_hour):
            ids.append(row["personId"])
    return ids


def write_params(output_file, slots, persons):
    """Write parameter entries to a single output file."""
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(["slot_index", "date", "start_hour", "end_hour", "person_count", "person_ids"])

        for i, (date_str, sh, eh) in enumerate(slots):
            ids = filter_persons(persons, date_str, sh, eh)
            ids_str = ",".join(ids) if ids else ""
            writer.writerow([i + 1, date_str, sh, eh, len(ids), ids_str])


def main():
    args = parse_args()

    print(f"Loading persons from: {args.input}")
    persons = load_persons(args.input)
    print(f"Loaded {len(persons)} persons")

    slots = generate_slots(args.start_date, args.days)
    print(f"Generated {len(slots)} time slots "
          f"({args.start_date}, {args.days} days, half-day intervals)")

    # Generate one file per query (Q2, Q3, Q4) with identical content
    import os
    for qname in ["Q2_batch_params.csv", "Q3_batch_params.csv", "Q4_batch_params.csv"]:
        output_path = os.path.join(args.output_dir, qname)
        write_params(output_path, slots, persons)
        print(f"Wrote {len(slots)} parameter entries to: {output_path}")


if __name__ == "__main__":
    main()
