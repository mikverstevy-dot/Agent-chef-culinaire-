"""C = C_hard ∪ C_soft. Violation dure → E = +∞."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

INF = float("inf")


@dataclass
class Constraint:
    id: str
    kind: str  # hard | soft
    type: str  # forbid_ingredient, max_time, servings, ...
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConstraintSet:
    items: list[Constraint] = field(default_factory=list)

    @property
    def hard(self) -> list[Constraint]:
        return [c for c in self.items if c.kind == "hard"]

    @property
    def soft(self) -> list[Constraint]:
        return [c for c in self.items if c.kind == "soft"]


def evaluate_gap(state, constraints: ConstraintSet) -> float:
    """E(R,C). Pas de formule unique forcée au-delà du testable."""
    names = {e.name.lower() for e in state.entities.values()}
    for c in constraints.hard:
        if c.type == "forbid_ingredient":
            banned = str(c.payload.get("name", "")).lower()
            if banned and banned in names:
                return INF
        if c.type == "ingredient_unavailable":
            # R0 ne peut pas contenir un ingrédient marqué indisponible
            name = str(c.payload.get("name", "")).lower()
            if name and name in names:
                return INF
        if c.type == "max_steps":
            nmax = c.payload.get("n")
            if nmax is not None and len(state.history) > int(nmax):
                return INF
    gap = 0.0
    for c in constraints.soft:
        if c.type == "prefer_ingredient":
            name = str(c.payload.get("name", "")).lower()
            if name not in names:
                gap += float(c.payload.get("weight", 1.0))
    return gap


def admissible(state, constraints: ConstraintSet) -> bool:
    return evaluate_gap(state, constraints) != INF
