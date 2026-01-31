# FinBench Query Parameters

## Overview

The original FinBench queries accept a single entity ID per invocation. We modified Q1–Q4 to accept batch ID inputs (`WHERE ... IN {input_ids}`), so each invocation processes a group of entities at once.

The two generator scripts produce 120 parameter sets each by slicing the entity `createTime` into time-based slots (UTC+8). This yields 120 × 4 = 480 total parameter sets across Q1–Q4.

## Source Data

Place the original FinBench snapshot files under `sf10/snapshot/`:
- `Account.csv` — source for Q1 parameters
- `Person.csv` — source for Q2, Q3, Q4 parameters

See [datasets/FinBench](../../../datasets/FinBench/) for how to download and prepare these files.

## Generating Parameters

### Q1 (Account IDs)

```bash
python3 gen_batch_account_params.py \
    --input sf10/snapshot/Account.csv \
    --output sf10/snapshot/Q1_batch_params.csv \
    --start-date 2021-12-22 \
    --days 10
```

Splits 10 days into 2-hour slots: 10 days × 12 slots/day = **120 parameter sets**.

### Q2, Q3, Q4 (Person IDs)

```bash
python3 gen_batch_person_params.py \
    --input sf10/snapshot/Person.csv \
    --output-dir sf10/snapshot/ \
    --start-date 2021-11-01 \
    --days 60
```

Splits 60 days into half-day slots (00–12, 12–24): 60 days × 2 slots/day = **120 parameter sets**. Generates three identical files: `Q2_batch_params.csv`, `Q3_batch_params.csv`, `Q4_batch_params.csv`.

## Output Format

Pipe-delimited CSV:

```
slot_index|date|start_hour|end_hour|count|ids
1|2021-12-22|0|2|15|id1,id2,...
```

The `ids` column is a comma-separated list of entity IDs, used directly as the `{input_ids}` placeholder in query templates.
