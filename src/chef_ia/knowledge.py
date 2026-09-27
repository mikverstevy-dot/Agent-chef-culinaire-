"""Atome de connaissance κ = <contenu, domaine, statut, confiance, source>."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from chef_ia.epistemics import EpistemicStatus, UNKNOWN


ELEMENT_TYPES = (
    "ENTITE",
    "RELATION",
    "TRANSFORMATION",
    "REGLE",
    "SEUIL",
    "QUANTITE",
    "PROPRIETE",
    "PROCESSUS",
    "NUTRITION",
    "SECURITE",
    "AUTRE_TYPE_JUSTIFIE",
)


@dataclass
class Traceability:
    document_id: str
    page: Optional[int] = None
    section: Optional[str] = None
    citation: Optional[str] = None  # formulation source, jamais « normalisée » en fait
    url: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    consulted_at: Optional[str] = None

    def is_exploitable(self) -> bool:
        return bool(self.document_id) and (
            self.page is not None or self.section or self.citation or self.url
        )


@dataclass
class KnowledgeAtom:
    id: str
    type_element: str
    content: dict[str, Any]
    domain: str
    status: EpistemicStatus
    confidence: Optional[float]  # UNKNOWN si None — jamais inventé
    trace: Traceability
    premises: list[str] = field(default_factory=list)  # ids pour DEDUIT
    uncertainty: Optional[dict[str, Any]] = None
    original_wording: Optional[str] = None

    def __post_init__(self) -> None:
        if self.type_element not in ELEMENT_TYPES:
            raise ValueError(f"type_element inconnu: {self.type_element}")
        if self.status == EpistemicStatus.DEDUIT and not self.premises:
            raise ValueError(f"{self.id}: DEDUIT exige des prémisses")
        if not self.trace.is_exploitable():
            raise ValueError(f"{self.id}: provenance non exploitable — non validée")
        if self.confidence is not None and not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confiance hors [0,1] — ne pas inventer une échelle")

    def as_usable_fact(self) -> bool:
        """A_VERIFIER et UNKNOWN ne sont pas des faits certains."""
        return self.status in (
            EpistemicStatus.EXPLICITE,
            EpistemicStatus.DEDUIT,
            EpistemicStatus.APPROXIME_EMPIRIQUE,
            EpistemicStatus.EXTERNE,
        ) and self.status != EpistemicStatus.A_VERIFIER


@dataclass
class Conflict:
    """Contradiction explicite — jamais résolue par moyenne arbitraire."""

    id: str
    atom_ids: list[str]
    description: str
    status: EpistemicStatus = EpistemicStatus.A_VERIFIER
    resolution_rule_id: Optional[str] = None


class KnowledgeBase:
    def __init__(self) -> None:
        self.atoms: dict[str, KnowledgeAtom] = {}
        self.conflicts: dict[str, Conflict] = {}
        self.by_document: dict[str, list[str]] = {}

    def add(self, atom: KnowledgeAtom) -> None:
        if atom.id in self.atoms:
            raise ValueError(f"id dupliqué: {atom.id}")
        self.atoms[atom.id] = atom
        self.by_document.setdefault(atom.trace.document_id, []).append(atom.id)

    def get(self, kid: str) -> Optional[KnowledgeAtom]:
        return self.atoms.get(kid)

    def relevant(self, tags: set[str]) -> list[KnowledgeAtom]:
        out = []
        for a in self.atoms.values():
            blob = " ".join(str(v) for v in a.content.values()).lower()
            if any(t.lower() in blob or t.lower() in a.domain.lower() for t in tags):
                out.append(a)
        return out

    def usable_for_automation(self, atom: KnowledgeAtom) -> bool:
        if atom.status == EpistemicStatus.A_VERIFIER:
            return False
        for c in self.conflicts.values():
            if atom.id in c.atom_ids and not c.resolution_rule_id:
                return False
        return True
