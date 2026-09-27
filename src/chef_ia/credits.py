"""Modèle de crédits configurable. Prix définitifs NON figés.

Week-end (sam+dim, TZ utilisateur) = gratuit pour l'utilisateur,
sans annuler les protections anti-abus.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class CreditEstimate:
    units: float
    weekend_free: bool
    message: str
    breakdown: dict[str, float]


# Coefficients *configurables* — pas des prix métier définitifs.
DEFAULT_WEIGHTS = {
    "n_hard_constraints": 1.0,
    "n_soft_constraints": 0.3,
    "n_ingredients": 0.5,
    "n_knowledge_consulted": 0.2,
    "n_steps": 0.4,
    "nutrition": 1.5,
    "external_search": 3.0,
}


def is_weekend(now: datetime, tz: str = "Africa/Libreville") -> bool:
    local = now.astimezone(ZoneInfo(tz))
    return local.weekday() >= 5  # 5=sam, 6=dim


def estimate(
    *,
    n_hard: int,
    n_soft: int,
    n_ingredients: int,
    n_knowledge: int,
    n_steps: int,
    nutrition: bool,
    external_search: bool,
    now: datetime,
    tz: str = "Africa/Libreville",
    weights: dict[str, float] | None = None,
    abuse_cap: float = 10_000.0,
) -> CreditEstimate:
    w = dict(DEFAULT_WEIGHTS)
    if weights:
        w.update(weights)
    bd = {
        "hard": n_hard * w["n_hard_constraints"],
        "soft": n_soft * w["n_soft_constraints"],
        "ingredients": n_ingredients * w["n_ingredients"],
        "knowledge": n_knowledge * w["n_knowledge_consulted"],
        "steps": n_steps * w["n_steps"],
        "nutrition": w["nutrition"] if nutrition else 0.0,
        "external": w["external_search"] if external_search else 0.0,
    }
    units = min(sum(bd.values()), abuse_cap)
    free = is_weekend(now, tz)
    if free:
        msg = f"Week-end : génération gratuite pour l'utilisateur (complexité interne ≈ {units:.1f} unités, plafond anti-abus {abuse_cap})."
    else:
        msg = f"Cette génération nécessite environ {units:.1f} crédits (tarifs non définitifs — calibration requise)."
    return CreditEstimate(units=units, weekend_free=free, message=msg, breakdown=bd)
