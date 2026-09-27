"""Nutrition uniquement à partir de données documentées.

N_k,100g = (N_k,total / M_final) * 100
Rétention : seulement si documentée ou hypothèse explicite A_VERIFIER.
"""

from __future__ import annotations

from typing import Any

from chef_ia.epistemics import UNKNOWN


def mass_final(masses_g: list[Any], documented_losses_g: list[Any] | None = None) -> Any:
    if any(m is UNKNOWN or m is None for m in masses_g):
        return UNKNOWN
    total = sum(float(m) for m in masses_g)
    if documented_losses_g is None:
        return total  # pas de perte inventée
    if any(x is UNKNOWN or x is None for x in documented_losses_g):
        return UNKNOWN
    return total - sum(float(x) for x in documented_losses_g)


def nutrient_total(contributions: list[Any]) -> Any:
    if any(c is UNKNOWN or c is None for c in contributions):
        return UNKNOWN
    return sum(float(c) for c in contributions)


def per_100g(n_total: Any, m_final: Any) -> Any:
    if n_total is UNKNOWN or m_final is UNKNOWN:
        return UNKNOWN
    if float(m_final) == 0:
        return UNKNOWN
    return (float(n_total) / float(m_final)) * 100.0


def apply_retention(n: Any, factor: Any, documented: bool) -> Any:
    if not documented:
        return UNKNOWN
    if n is UNKNOWN or factor is UNKNOWN or factor is None:
        return UNKNOWN
    return float(n) * float(factor)
