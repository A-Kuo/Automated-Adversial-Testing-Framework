"""Coverage metric tracker for the dynamic mutation engine."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rtaas.attack_engine.library import Attack


class CoverageTracker:
    """
    Tracks which harm categories have been successfully attacked vs. tested.

    Drives the mutation engine to prioritize under-covered categories.
    """

    def __init__(self, attacks: list[Attack]) -> None:
        self.all_categories: set[str] = {a.harm_category for a in attacks}
        self._tested: dict[str, int] = defaultdict(int)
        self._failed: dict[str, int] = defaultdict(int)

    def record(self, attack: Attack, severity: str) -> None:
        self._tested[attack.harm_category] += 1
        if severity != "PASS":
            self._failed[attack.harm_category] += 1

    @property
    def coverage(self) -> float:
        """Fraction of harm categories that have been tested at least once."""
        if not self.all_categories:
            return 1.0
        tested = sum(1 for c in self.all_categories if self._tested[c] > 0)
        return tested / len(self.all_categories)

    @property
    def under_covered_categories(self) -> list[str]:
        """Categories with zero or low failure rates — mutation targets."""
        return [
            c for c in self.all_categories
            if self._tested[c] == 0 or (self._failed[c] / self._tested[c]) < 0.1
        ]

    def summary(self) -> dict:
        return {
            "coverage": round(self.coverage, 3),
            "categories_tested": len(self._tested),
            "categories_total": len(self.all_categories),
            "by_category": {
                c: {"tested": self._tested[c], "failed": self._failed[c]}
                for c in sorted(self.all_categories)
            },
        }
