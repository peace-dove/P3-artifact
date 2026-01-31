#!/usr/bin/env python3
"""Generate 120 batch input parameter sets from Account.csv.

Scans a 10-day window (e.g. 2021-12-22 to 2021-12-31), splitting each day
into 12 two-hour slots (00-02, 02-04, ..., 22-24), producing 10 * 12 = 120
parameter entries. Each entry contains the account IDs whose createTime
falls within that slot (UTC+8).

Usage:
    python3 gen_batch_params.py [--input sf10/snapshot/Account.csv]
                                [--output Q1_batch_params.csv]
                                [--start-date 2021-12-22]
                                [--days 10]
"""

import csv
import argparse
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Generate batch input params from Account.csv")
    parser.add_argument("--input", default="sf10/snapshot/Account.csv",
                        help="Input Account CSV file (pipe-delimited)")
    parser.add_argument("--output", default="Q1_batch_params.csv",
                        help="Output parameter file")
    parser.add_argument("--start-date", default="2021-12-22",
                        help="First day of the window (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=10,
                        help="Number of days in the window")
    return parser.parse_args()


def load_accounts(input_file):
    """Load all accounts with their createTime converted to UTC+8 datetime."""
    accounts = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            try:
                ts_ms = int(row["createTime"])
                dt = datetime.utcfromtimestamp(ts_ms / 1000) + timedelta(hours=8)
                accounts.append((row, dt))
            except (ValueError, KeyError):
                continue
    return accounts


def generate_slots(start_date, num_days, slot_hours=2):
    """Generate (date_str, start_hour, end_hour) tuples.

    10 days * 12 slots/day = 120 slots.
    """
    slots = []
    base = datetime.strptime(start_date, "%Y-%m-%d")
    for day_offset in range(num_days):
        current_date = base + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        for hour in range(0, 24, slot_hours):
            slots.append((date_str, hour, hour + slot_hours))
    return slots


def filter_accounts(accounts, target_date, start_hour, end_hour):
    """Return account IDs matching the given date and hour range (UTC+8)."""
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    ids = []
    for row, dt in accounts:
        if (dt.year == target_dt.year
                and dt.month == target_dt.month
                and dt.day == target_dt.day
                and start_hour <= dt.hour < end_hour):
            ids.append(row["accountId"])
    return ids


def main():
    args = parse_args()

    print(f"Loading accounts from: {args.input}")
    accounts = load_accounts(args.input)
    print(f"Loaded {len(accounts)} accounts")

    slots = generate_slots(args.start_date, args.days)
    print(f"Generated {len(slots)} time slots "
          f"({args.start_date} to {args.days} days, 2-hour intervals)")

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(["slot_index", "date", "start_hour", "end_hour", "account_count", "account_ids"])

        for i, (date_str, sh, eh) in enumerate(slots):
            ids = filter_accounts(accounts, date_str, sh, eh)
            ids_str = ",".join(ids) if ids else ""
            writer.writerow([i + 1, date_str, sh, eh, len(ids), ids_str])

    print(f"Wrote {len(slots)} parameter entries to: {args.output}")


if __name__ == "__main__":
    main()
