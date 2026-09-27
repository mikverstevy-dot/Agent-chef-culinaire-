"""O(R0, C, K) — V0 : recherche bornée, pas de solveur lourd.

R_{n+1} = T(R_n, a_n), a_n ∈ A(R_n, K)
Arrêt : R_n ∈ Ω et E ≤ ε, n ≤ Nmax
Si insuffisant : INSUFFICIENT_KNOWLEDGE — jamais d'invention.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from chef_ia.constraints import Constraint, ConstraintSet, INF, admissible, evaluate_gap
from chef_ia.epistemics import EpistemicStatus, UNKNOWN
from chef_ia.knowledge import KnowledgeBase
from chef_ia.state import Action, CulinaryState, Entity


@dataclass
class GenerationResult:
    ok: bool
    reason: str
    trajectory: list[CulinaryState] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    gap: float = INF
    used_knowledge: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    insufficient: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "reason": self.reason,
            "n_steps": len(self.actions),
            "gap": self.gap if self.gap != INF else "INF",
            "used_knowledge": self.used_knowledge,
            "uncertainties": self.uncertainties,
            "insufficient": self.insufficient,
            "history": [s.history for s in self.trajectory[1:]],
        }


class CulinaryEngine:
    def __init__(self, kb: KnowledgeBase, epsilon: float = 0.0, nmax: int = 32, lam: float = 0.1):
        self.kb = kb
        self.epsilon = epsilon
        self.nmax = nmax
        self.lam = lam

    def admissible_actions(self, state: CulinaryState) -> list[Action]:
        """A(R,K) — uniquement actions justifiées par K utilisable, plus ajouts R0."""
        actions: list[Action] = []
        for atom in self.kb.atoms.values():
            if not self.kb.usable_for_automation(atom):
                continue
            if atom.status == EpistemicStatus.A_VERIFIER:
                continue
            if atom.type_element == "TRANSFORMATION":
                t = atom.content.get("action_type")
                if not t:
                    continue
                cond = atom.content.get("condition")
                if cond and not self._condition_holds(state, cond, atom):
                    continue
                actions.append(
                    Action(type=str(t), params=dict(atom.content), knowledge_ids=[atom.id])
                )
        return actions

    def _condition_holds(self, state: CulinaryState, cond: Any, atom) -> bool:
        """Condition non évaluable → False (pas d'hypothèse vraie)."""
        if cond is UNKNOWN or cond is None:
            return False
        if isinstance(cond, dict):
            need = cond.get("requires_entity")
            if need and need.lower() not in {e.name.lower() for e in state.entities.values()}:
                return False
        return True

    def generate(self, r0: CulinaryState, constraints: ConstraintSet) -> GenerationResult:
        if not admissible(r0, constraints):
            return GenerationResult(
                ok=False,
                reason="état initial viole une contrainte dure",
                trajectory=[r0],
                gap=INF,
            )

        if len(self.kb.atoms) == 0 and not r0.entities:
            return GenerationResult(
                ok=False,
                reason="connaissances disponibles insuffisantes",
                trajectory=[r0],
                insufficient=True,
            )

        # V0 : trajectoire triviale = R0 si déjà admissible et E≤ε
        e0 = evaluate_gap(r0, constraints)
        traj = [r0]
        acts: list[Action] = []
        used: list[str] = []
        uncert: list[str] = []

        state = r0
        n = 0
        while n < self.nmax and not (admissible(state, constraints) and evaluate_gap(state, constraints) <= self.epsilon):
            cands = self.admissible_actions(state)
            if not cands:
                break
            # J = E + λ Length — choix glouton V0
            best = None
            best_j = INF
            for a in cands:
                nxt = state.apply_action(a)
                if not admissible(nxt, constraints):
                    continue
                j = evaluate_gap(nxt, constraints) + self.lam * (n + 1)
                if j < best_j:
                    best_j = j
                    best = (a, nxt)
            if best is None:
                break
            a, state = best
            acts.append(a)
            used.extend(a.knowledge_ids)
            traj.append(state)
            n += 1

        gap = evaluate_gap(state, constraints)
        if admissible(state, constraints) and gap <= self.epsilon:
            return GenerationResult(
                ok=True,
                reason="trajectoire admissible",
                trajectory=traj,
                actions=acts,
                gap=gap,
                used_knowledge=used,
                uncertainties=uncert,
            )

        if admissible(state, constraints):
            return GenerationResult(
                ok=False,
                reason="meilleur état admissible trouvé mais E > ε — connaissances insuffisantes pour l'objectif",
                trajectory=traj,
                actions=acts,
                gap=gap,
                used_knowledge=used,
                insufficient=True,
            )

        return GenerationResult(
            ok=False,
            reason="aucune solution suffisamment justifiée",
            trajectory=traj,
            actions=acts,
            gap=gap,
            used_knowledge=used,
            insufficient=True,
        )


def parse_user_intent(text: str) -> tuple[CulinaryState, ConstraintSet]:
    """Interprétation minimale déterministe (pas un LLM). Pas d'invention d'ingrédients."""
    r0 = CulinaryState()
    cs = ConstraintSet()
    # Format volontairement strict : "ingredients: a, b | forbid: c | servings: 2"
    parts = [p.strip() for p in text.split("|")]
    idx = 0
    for p in parts:
        if p.lower().startswith("ingredients:"):
            raw = p.split(":", 1)[1]
            for name in [x.strip() for x in raw.split(",") if x.strip()]:
                eid = f"e{idx}"
                idx += 1
                r0.entities[eid] = Entity(id=eid, name=name, mass_g=UNKNOWN)
        elif p.lower().startswith("forbid:"):
            raw = p.split(":", 1)[1]
            for name in [x.strip() for x in raw.split(",") if x.strip()]:
                cs.items.append(
                    Constraint(
                        id=f"h-{name}",
                        kind="hard",
                        type="forbid_ingredient",
                        payload={"name": name},
                    )
                )
        elif p.lower().startswith("prefer:"):
            raw = p.split(":", 1)[1]
            for name in [x.strip() for x in raw.split(",") if x.strip()]:
                cs.items.append(
                    Constraint(
                        id=f"s-{name}",
                        kind="soft",
                        type="prefer_ingredient",
                        payload={"name": name},
                    )
                )
    return r0, cs
