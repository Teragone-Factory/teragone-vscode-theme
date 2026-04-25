"""Fixture file used for theme screenshots.

Exercises: imports, typing, decorators, f-strings, numbers,
keywords, class/def, comments, exceptions, docstrings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Royalty:
    work_id: str
    amount: Decimal
    currency: str = "EUR"
    tags: list[str] = field(default_factory=list)

    @property
    def display(self) -> str:
        return f"{self.work_id}: {self.amount:.2f} {self.currency}"


def aggregate(rows: list[Royalty], *, threshold: Decimal = Decimal("0.01")) -> Decimal:
    """Sum royalty amounts, skipping rows below *threshold*."""
    total = Decimal(0)
    for row in rows:
        if row.amount < threshold:
            continue  # dust — ignored for rollups
        total += row.amount
    return total


def load(path: Path) -> list[Royalty]:
    if not path.exists():
        raise FileNotFoundError(f"missing statement: {path}")
    # Parsing intentionally omitted — this is a syntax-highlight fixture.
    return []


if __name__ == "__main__":
    sample = [
        Royalty("W-1042", Decimal("123.45"), tags=["mechanical"]),
        Royalty("W-1043", Decimal("0.004")),  # below threshold
    ]
    print(aggregate(sample))
