from __future__ import annotations

from dataclasses import dataclass

from .tools import AnalyticsTools, Metric


def percent_change(current: float, previous: float) -> float:
    return ((current - previous) / previous * 100) if previous else 0.0


@dataclass
class Finding:
    dimension: str
    member: str
    revenue_change: float
    contribution: float


class InvestigationAgent:
    """A transparent decide -> call tool -> observe loop.

    The policy is intentionally deterministic so a learner can trace every choice.
    It first checks headline metrics, then tests each business dimension, and ranks
    the segment contributions to the total revenue movement.
    """

    dimensions = ("category", "region", "channel")

    def __init__(self, tools: AnalyticsTools):
        self.tools = tools
        self.trace: list[str] = []

    def investigate(self, current_date: str, previous_date: str) -> str:
        self.trace.clear()
        previous = self._call_summary(previous_date)
        current = self._call_summary(current_date)
        total_change = current.revenue - previous.revenue

        findings: list[Finding] = []
        for dimension in self.dimensions:
            self.trace.append(f"DECIDE: inspect {dimension} to localize the change")
            old_groups = self._call_breakdown(previous_date, dimension)
            new_groups = self._call_breakdown(current_date, dimension)
            for member in old_groups.keys() | new_groups.keys():
                change = new_groups.get(member, Metric(0, 0)).revenue - old_groups.get(member, Metric(0, 0)).revenue
                findings.append(Finding(dimension, member, change, change / total_change if total_change else 0))

        primary = min(findings, key=lambda item: item.revenue_change)
        return self._report(previous_date, current_date, previous, current, primary)

    def _call_summary(self, date: str) -> Metric:
        self.trace.append(f"CALL: metric_summary(date={date})")
        result = self.tools.metric_summary(date)
        self.trace.append(f"OBSERVE: revenue={result.revenue:.0f}, orders={result.orders}, AOV={result.average_order_value:.2f}")
        return result

    def _call_breakdown(self, date: str, dimension: str) -> dict[str, Metric]:
        self.trace.append(f"CALL: breakdown(date={date}, dimension={dimension})")
        return self.tools.breakdown(date, dimension)

    def _report(self, previous_date: str, current_date: str, previous: Metric, current: Metric, primary: Finding) -> str:
        return "\n".join([
            "INVESTIGATION SUMMARY",
            f"Period: {previous_date} -> {current_date}",
            f"Revenue: ${previous.revenue:,.0f} -> ${current.revenue:,.0f} ({percent_change(current.revenue, previous.revenue):+.1f}%)",
            f"Orders: {previous.orders:,} -> {current.orders:,} ({percent_change(current.orders, previous.orders):+.1f}%)",
            f"Average order value: ${previous.average_order_value:,.2f} -> ${current.average_order_value:,.2f} ({percent_change(current.average_order_value, previous.average_order_value):+.1f}%)",
            "",
            f"Primary driver: {primary.dimension} = {primary.member}",
            f"Evidence: this segment changed revenue by ${primary.revenue_change:,.0f}.",
            "Conclusion: the revenue movement is primarily a mix/value problem, not an order-volume problem." if abs(percent_change(current.orders, previous.orders)) < abs(percent_change(current.revenue, previous.revenue)) else "Conclusion: order volume is a material driver of the revenue movement.",
        ])

