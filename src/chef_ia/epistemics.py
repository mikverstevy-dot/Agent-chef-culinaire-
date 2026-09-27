"""Statuts épistémiques — non optionnels, non fusionnables."""

from __future__ import annotations

from enum import Enum
from typing import Any


class EpistemicStatus(str, Enum):
    EXPLICITE = "EXPLICITE"
    DEDUIT = "DEDUIT"
    APPROXIME_EMPIRIQUE = "APPROXIME_EMPIRIQUE"
    A_VERIFIER = "A_VERIFIER"
    EXTERNE = "EXTERNE"


UNKNOWN = "UNKNOWN"


def never_invent(value: Any) -> Any:
    """Toute valeur absente reste UNKNOWN. Aucune borne inventée."""
    if value is None or value == "":
        return UNKNOWN
    return value


def cannot_promote_to_explicit(*_premises: Any) -> EpistemicStatus:
    """A, B, C séparés ne deviennent jamais une loi EXPLICITE."""
    return EpistemicStatus.DEDUIT
