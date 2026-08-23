from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Metric:
    orders: int
    revenue: float

    @property
    def average_order_value(self) -> float:
        return self.revenue / self.orders if self.orders else 0.0


class AnalyticsTools:
    """The agent's small tool belt: metric totals and dimensional breakdowns."""

    def __init__(self, data_path: str | Path):
        with Path(data_path).open(newline="", encoding="utf-8") as handle:
            self.rows = list(csv.DictReader(handle))

    def available_dates(self) -> list[str]:
        return sorted({row["date"] for row in self.rows})

    def metric_summary(self, date: str) -> Metric:
        return self._aggregate(row for row in self.rows if row["date"] == date)

    def breakdown(self, date: str, dimension: str) -> dict[str, Metric]:
        if dimension not in {"region", "channel", "category"}:
            raise ValueError(f"Unsupported dimension: {dimension}")
        groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in self.rows:
            if row["date"] == date:
                groups[row[dimension]].append(row)
        return {name: self._aggregate(rows) for name, rows in sorted(groups.items())}

    @staticmethod
    def _aggregate(rows) -> Metric:
        rows = list(rows)
        return Metric(
            orders=sum(int(row["orders"]) for row in rows),
            revenue=sum(float(row["revenue"]) for row in rows),
        )

