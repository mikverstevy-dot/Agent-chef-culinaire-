"""État culinaire R = <M, Φ, Ψ, Υ, H>. Valeurs inconnues = UNKNOWN."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from chef_ia.epistemics import UNKNOWN


@dataclass
class Entity:
    id: str
    name: str
    mass_g: Any = UNKNOWN
    volume_ml: Any = UNKNOWN
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for k, v in list(self.properties.items()):
            if v is None:
                self.properties[k] = UNKNOWN


@dataclass
class CulinaryState:
    entities: dict[str, Entity] = field(default_factory=dict)
    phi: dict[str, Any] = field(default_factory=dict)  # thermo / physico-chimique
    psi: dict[str, Any] = field(default_factory=dict)  # texture
    upsilon: dict[str, Any] = field(default_factory=dict)  # nutrition
    history: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        for d in (self.phi, self.psi, self.upsilon):
            for k, v in list(d.items()):
                if v is None:
                    d[k] = UNKNOWN

    def copy(self) -> "CulinaryState":
        import copy

        return copy.deepcopy(self)

    def apply_action(self, action: "Action") -> "CulinaryState":
        nxt = self.copy()
        nxt.history.append({"action": action.as_dict()})
        if action.type == "ajouter" and action.entity:
            e = action.entity
            nxt.entities[e.id] = e
        elif action.type == "retirer" and action.target_id:
            nxt.entities.pop(action.target_id, None)
        # Autres transformations : uniquement si une règle K documentée s'applique (moteur).
        return nxt


@dataclass
class Action:
    type: str
    params: dict[str, Any] = field(default_factory=dict)
    entity: Optional[Entity] = None
    target_id: Optional[str] = None
    knowledge_ids: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "params": self.params,
            "target_id": self.target_id,
            "knowledge_ids": list(self.knowledge_ids),
        }
