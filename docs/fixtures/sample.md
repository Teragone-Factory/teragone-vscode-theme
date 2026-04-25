# Royalty Statement — Q3 2026

Short prose fixture used to capture the **Teragone Factory** markdown
preview. Exercises headings, lists, blockquote, inline code, table,
links, and a fenced code block.

## Summary

- Total works processed: **1 042**
- Rows below the `0.01 EUR` threshold: 37 (skipped)
- Reconciled against the provider statement on *2026-04-15*

> Rows below threshold are retained in the raw archive but excluded
> from the rollup — see `aggregate()` in `sample.py`.

## Breakdown

| Source       | Works | Amount (EUR) |
|--------------|------:|-------------:|
| Streaming    |   812 |     9 214.57 |
| Downloads    |   188 |     1 106.20 |
| Sync & other |    42 |       873.11 |
| **Total**    | 1 042 |    11 193.88 |

## Reproduction

```bash
uv run python sample.py \
  --input statements/q3-2026.json \
  --threshold 0.01
```

See the [aggregation notes](./sample.py) for the exact rounding rules.
