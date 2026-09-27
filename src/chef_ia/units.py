"""Analyse dimensionnelle déterministe. Pas d'addition T + masse."""

from __future__ import annotations

from dataclasses import dataclass


class DimensionError(ValueError):
    pass


# Unités documentées ici comme *catalogue de conversion*, pas comme faits culinaires.
# Les conversions SI de base sont des définitions métrologiques, pas des inventions scientifiques culinaires.
CONVERSION_TO_SI = {
    ("g", "mass"): 0.001,  # kg
    ("kg", "mass"): 1.0,
    ("mg", "mass"): 1e-6,
    ("l", "volume"): 0.001,  # m3
    ("ml", "volume"): 1e-6,
    ("s", "time"): 1.0,
    ("min", "time"): 60.0,
    ("h", "time"): 3600.0,
    ("K", "temperature"): 1.0,  # stocké en K uniquement après conversion explicite
}

DIMENSION_OF = {
    "g": "mass",
    "kg": "mass",
    "mg": "mass",
    "l": "volume",
    "ml": "volume",
    "s": "time",
    "min": "time",
    "h": "time",
    "K": "temperature",
    "C": "temperature",
    "degC": "temperature",
}


@dataclass(frozen=True)
class Qty:
    value: float
    unit: str
    original_unit: str

    @property
    def dimension(self) -> str:
        if self.unit not in DIMENSION_OF:
            raise DimensionError(f"unité inconnue (pas inventée): {self.unit}")
        return DIMENSION_OF[self.unit]


def add(a: Qty, b: Qty) -> Qty:
    if a.dimension != b.dimension:
        raise DimensionError(f"addition incompatible: {a.dimension} + {b.dimension}")
    if a.unit != b.unit:
        raise DimensionError("conversion requise avant addition — unités originales conservées")
    return Qty(a.value + b.value, a.unit, a.original_unit)


def celsius_to_kelvin(c: float) -> Qty:
    """Conversion métrologique T(K) = t(°C) + 273.15 — définition, pas fait culinaire."""
    return Qty(c + 273.15, "K", "degC")
