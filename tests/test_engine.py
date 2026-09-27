from chef_ia.constraints import Constraint, ConstraintSet, INF, evaluate_gap
from chef_ia.engine import CulinaryEngine, parse_user_intent
from chef_ia.epistemics import EpistemicStatus, UNKNOWN
from chef_ia.knowledge import KnowledgeAtom, KnowledgeBase, Traceability
from chef_ia.state import CulinaryState, Entity
from chef_ia.units import Qty, add, DimensionError, celsius_to_kelvin
from chef_ia.nutrition import apply_retention, mass_final, per_100g
from chef_ia.fusion import FusionError, fuse
from chef_ia.credits import estimate, is_weekend
from datetime import datetime, timezone
import pytest


def test_A_simple_recipe_r0_admissible():
    r0, c = parse_user_intent("ingredients: oeuf, farine")
    res = CulinaryEngine(KnowledgeBase()).generate(r0, c)
    assert res.ok
    assert res.gap == 0.0


def test_B_multiple_constraints():
    r0, c = parse_user_intent("ingredients: oeuf | forbid: arachide | prefer: citron")
    res = CulinaryEngine(KnowledgeBase(), epsilon=0.0).generate(r0, c)
    assert not res.ok
    assert res.insufficient
    assert res.gap > 0
    assert res.gap != float("inf")  # hard OK (arachide absent)


def test_C_missing_ingredients_unknown_mass():
    r0, _ = parse_user_intent("ingredients: tomate")
    e = next(iter(r0.entities.values()))
    assert e.mass_g == UNKNOWN


def test_D_insufficient_knowledge():
    r0 = CulinaryState()
    res = CulinaryEngine(KnowledgeBase()).generate(r0, ConstraintSet())
    assert res.insufficient
    assert "insuffisant" in res.reason.lower()


def test_E_contradiction_blocks_automation():
    kb = KnowledgeBase()
    t = Traceability(document_id="d1", page=1, citation="A")
    a = KnowledgeAtom(
        id="k1",
        type_element="REGLE",
        content={"x": 1},
        domain="test",
        status=EpistemicStatus.EXPLICITE,
        confidence=None,
        trace=t,
    )
    b = KnowledgeAtom(
        id="k2",
        type_element="REGLE",
        content={"x": 2},
        domain="test",
        status=EpistemicStatus.EXPLICITE,
        confidence=None,
        trace=Traceability(document_id="d2", page=1, citation="B"),
    )
    kb.add(a)
    kb.add(b)
    from chef_ia.fusion import register_conflict

    register_conflict(kb, "k1", "k2", "x diverge")
    assert not kb.usable_for_automation(a)


def test_F_approximate_not_exact_threshold():
    atom = KnowledgeAtom(
        id="k-approx",
        type_element="SEUIL",
        content={"wording": "vers 140 °C", "T": UNKNOWN},
        domain="maillard",
        status=EpistemicStatus.APPROXIME_EMPIRIQUE,
        confidence=None,
        trace=Traceability(document_id="p1", page=2, citation="vers 140 °C"),
        original_wording="vers 140 °C",
        uncertainty={"note": "formulation source conservée"},
    )
    assert atom.content["T"] == UNKNOWN
    assert atom.status == EpistemicStatus.APPROXIME_EMPIRIQUE


def test_G_externe_status_exists():
    assert EpistemicStatus.EXTERNE.value == "EXTERNE"


def test_H_nutrition_no_invented_retention():
    assert apply_retention(10, 0.8, documented=False) == UNKNOWN
    assert mass_final([UNKNOWN, 10]) == UNKNOWN
    assert per_100g(10, 50) == 20.0


def test_I_units_forbid_T_plus_mass():
    t = celsius_to_kelvin(20)
    m = Qty(100, "g", "g")
    with pytest.raises(DimensionError):
        add(t, m)


def test_J_rule_needs_premises_for_deduit():
    with pytest.raises(ValueError):
        KnowledgeAtom(
            id="bad",
            type_element="REGLE",
            content={},
            domain="x",
            status=EpistemicStatus.DEDUIT,
            confidence=None,
            trace=Traceability(document_id="d", page=1, citation="c"),
        )


def test_K_traceability_required():
    with pytest.raises(ValueError):
        KnowledgeAtom(
            id="bad2",
            type_element="ENTITE",
            content={},
            domain="x",
            status=EpistemicStatus.EXPLICITE,
            confidence=None,
            trace=Traceability(document_id=""),
        )


def test_N_no_hallucinated_kb():
    kb = KnowledgeBase()
    assert list(kb.atoms) == []


def test_fusion_blocked_before_six():
    with pytest.raises(FusionError):
        fuse([])


def test_hard_forbid():
    r0, c = parse_user_intent("ingredients: arachide | forbid: arachide")
    assert evaluate_gap(r0, c) == INF


def test_L_credits_message():
    e = estimate(
        n_hard=1,
        n_soft=0,
        n_ingredients=2,
        n_knowledge=0,
        n_steps=3,
        nutrition=False,
        external_search=False,
        now=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),  # lundi
        tz="Africa/Libreville",
    )
    assert "crédits" in e.message.lower() or e.weekend_free


def test_M_weekend_libreville():
    # 2026-09-27 is Sunday
    assert is_weekend(datetime(2026, 9, 27, 12, tzinfo=timezone.utc), "Africa/Libreville")
