"""Fusion des extraits JSON.

Ne crée aucune loi nouvelle. Ne résout aucun conflit par moyenne.
Les documents non acceptés restent A_VERIFIER au niveau *jeu fusionné*.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


SECONDARY = {
    "PDF7_BOOKEY_MCGEE_RESUME",
    "PDF8_BOOKEY_WOLKE_RESUME",
}

EXCERPT = {"PDF2_CHARLES_CUISINE_EXPLIQUEE_EXTRAIT"}


def _norm(s: str) -> str:
    s = s.lower().replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_extractions(root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for d in sorted(root.glob("PDF*")):
        kj = d / "knowledge.json"
        if not kj.exists():
            continue
        chunk = json.loads(kj.read_text(encoding="utf-8"))
        items.extend(chunk)
    return items


def fuse_spans(items: list[dict[str, Any]], *, waiver: str) -> dict[str, Any]:
    """Dédup par libellé normalisé ; provenances multiples conservées."""
    if "A_VERIFIER" not in waiver:
        raise ValueError("fusion d'extraits non acceptés exige waiver A_VERIFIER")

    clusters: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for it in items:
        text = it.get("original_wording") or it.get("forme_logique", {}).get("text") or ""
        key = _norm(text)
        if len(key) < 8:
            continue
        doc = it["tracabilite"]["document_id"]
        rec = {
            "id": it["id_connaissance"],
            "document_id": doc,
            "page": it["tracabilite"].get("page"),
            "epistemologie_span": it["epistemologie"],
            "secondary_summary": doc in SECONDARY,
            "excerpt_only": doc in EXCERPT,
        }
        if key not in clusters:
            clusters[key] = {
                "canonical_wording": text,
                "normalized": key,
                "provenances": [rec],
                "n_docs": 1,
                "docs": {doc},
            }
            order.append(key)
        else:
            clusters[key]["provenances"].append(rec)
            clusters[key]["docs"].add(doc)

    fused = []
    for key in order:
        c = clusters[key]
        docs = sorted(c["docs"])
        fused.append(
            {
                "forme_logique": {"kind": "source_span", "text": c["canonical_wording"]},
                "n_occurrences": len(c["provenances"]),
                "documents": docs,
                "multi_document": len(docs) > 1,
                "provenances": c["provenances"][:20],  # cap audit
                "n_provenances": len(c["provenances"]),
                # Jeu fusionné non validé :
                "epistemologie_fusion": "A_VERIFIER",
                "contains_secondary_summary": any(
                    p["secondary_summary"] for p in c["provenances"]
                ),
            }
        )

    by_doc: dict[str, int] = defaultdict(int)
    for it in items:
        by_doc[it["tracabilite"]["document_id"]] += 1

    # Tensions DOCUMENTAIRES (pas des contradictions scientifiques tranchées)
    tensions = [
        {
            "id": "T-HIST-VS-NUTRI",
            "documents": ["PDF1_ESCOFFIER_1907", "PDF4_PNNS_GUIDE_ALIMENTAIRE", "PDF6_WFP_NUTRITION_2018"],
            "description": "Manuel 1907 vs guides nutrition 2002/2018 : régimes, sel, graisses, sécurité — ne pas homogénéiser.",
            "status": "A_VERIFIER",
            "resolution": None,
        },
        {
            "id": "T-BOOKEY-NOT-ORIGINAL",
            "documents": ["PDF7_BOOKEY_MCGEE_RESUME", "PDF8_BOOKEY_WOLKE_RESUME"],
            "description": "Résumés Bookey ≠ ouvrages McGee/Wolke. Interdit de citer comme EXPLICITE McGee/Wolke.",
            "status": "A_VERIFIER",
            "resolution": None,
        },
        {
            "id": "T-EXTRAIT-INCOMPLET",
            "documents": ["PDF2_CHARLES_CUISINE_EXPLIQUEE_EXTRAIT"],
            "description": "Couverture partielle de La Cuisine expliquée.",
            "status": "A_VERIFIER",
            "resolution": None,
        },
        {
            "id": "T-PDF5-ATTRIBUTION",
            "documents": ["PDF5_CUISINE_MOLECULAIRE_DOC"],
            "description": "Le span source peut écrire « Nicholas Curtis » ; aucune substitution automatique par Kurti.",
            "status": "A_VERIFIER",
            "resolution": None,
        },
    ]

    gaps = [
        {
            "id": "G-NO-TYPED-ONTOLOGY",
            "description": "Tous les spans sont AUTRE_TYPE_JUSTIFIE : pas d'ENTITE/PROPRIETE/TRANSFORMATION validées.",
        },
        {
            "id": "G-NO-GRAPH",
            "description": "Aucun graphe ingrédient→composé→condition→effet : le construire maintenant serait une inférence.",
        },
        {
            "id": "G-NO-SI-UNITS",
            "description": "Pas de normalisation SI des températures/durées (anti-invention des bornes).",
        },
        {
            "id": "G-NO-NUTRITION-TABLES",
            "description": "PDF4/PDF6 parlent nutrition mais les tableaux n'ont pas été atomisés en QUANTITE/NUTRITION.",
        },
        {
            "id": "G-CONTRADICTIONS-NUMERIQUES",
            "description": "Détection automatique de contradictions numériques non effectuée : trop d'OCR, risque d'inventer des conflits.",
        },
    ]

    return {
        "waiver": waiver,
        "n_spans_in": len(items),
        "n_clusters": len(fused),
        "n_multi_document_wordings": sum(1 for x in fused if x["multi_document"]),
        "by_document": dict(by_doc),
        "tensions_documentaires": tensions,
        "trous": gaps,
        "clusters": fused,
    }
