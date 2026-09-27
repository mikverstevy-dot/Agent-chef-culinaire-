"""Extraction PDF séquentielle. Pas de fusion avant validation des 6.

JSON = source de vérité. Rapport humain = vue du JSON.
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Optional

from chef_ia.epistemics import EpistemicStatus


@dataclass
class ExtractionItem:
    id_connaissance: str
    type_element: str
    forme_logique: dict[str, Any]
    epistemologie: str
    tracabilite: dict[str, Any]
    original_wording: str


@dataclass
class ExtractionReport:
    document_id: str
    path: str
    n_pages: int
    n_elements: int
    ids: list[str]
    coverage_notes: list[str]
    ambiguities: list[str]
    orphan_refs: list[str]
    numeric_fidelity_issues: list[str]
    accepted: bool
    score_notes: str


def _stable_id(document_id: str, page: int, text: str, i: int) -> str:
    h = hashlib.sha256(f"{document_id}|{page}|{i}|{text}".encode()).hexdigest()[:12]
    return f"{document_id}-p{page}-{h}"


def extract_pdf_text_pages(path: str) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(path)
    pages = []
    for p in reader.pages:
        pages.append(p.extract_text() or "")
    return pages


def extract_document(path: str, document_id: str) -> tuple[list[ExtractionItem], ExtractionReport]:
    """Extraction atomique conservative : un bloc texte → un atome EXPLICITE du texte,
    jamais une loi combinée.

    Sans ontologie métier du document, on n'invente pas d'entités culinaires.
    Les phrases candidates numériques/règles restent A_VERIFIER jusqu'à revue humaine
    (le test P1 100/100 était une extraction *revue*, pas une vérité scientifique auto).
    """
    pages = extract_pdf_text_pages(path)
    items: list[ExtractionItem] = []
    ambiguities: list[str] = []

    for pi, text in enumerate(pages, start=1):
        # Découpage par lignes non vides — pas de fusion inter-phrases.
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for i, line in enumerate(lines):
            if len(line) < 8:
                continue
            status = EpistemicStatus.EXPLICITE.value
            if any(w in line.lower() for w in ("vers ", "environ ", "environ", "approxim")):
                status = EpistemicStatus.APPROXIME_EMPIRIQUE.value
                ambiguities.append(f"page {pi}: formulation approximative conservée: {line[:120]}")
            kid = _stable_id(document_id, pi, line, i)
            items.append(
                ExtractionItem(
                    id_connaissance=kid,
                    type_element="AUTRE_TYPE_JUSTIFIE",
                    forme_logique={"kind": "source_span", "text": line},
                    epistemologie=status,
                    tracabilite={
                        "document_id": document_id,
                        "page": pi,
                        "section": None,
                        "citation": line,
                    },
                    original_wording=line,
                )
            )

    ids = [it.id_connaissance for it in items]
    orphan: list[str] = []
    report = ExtractionReport(
        document_id=document_id,
        path=path,
        n_pages=len(pages),
        n_elements=len(items),
        ids=ids,
        coverage_notes=[
            "Couverture = spans de texte extraits, pas d'interprétation scientifique automatique.",
            "Validation humaine requise avant enrichissement de K (règle §18).",
        ],
        ambiguities=ambiguities,
        orphan_refs=orphan,
        numeric_fidelity_issues=[],
        accepted=False,
        score_notes="non scorée automatiquement — le 100/100 P1 était un audit humain.",
    )
    return items, report


def save_extraction(out_dir: Path, items: list[ExtractionItem], report: ExtractionReport) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "knowledge.json").write_text(
        json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "report.json").write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "report.md").write_text(_report_md(report), encoding="utf-8")


def _report_md(r: ExtractionReport) -> str:
    return (
        f"# Rapport d'extraction — {r.document_id}\n\n"
        f"- pages: {r.n_pages}\n"
        f"- éléments: {r.n_elements}\n"
        f"- accepté: {r.accepted}\n"
        f"- {r.score_notes}\n\n"
        f"## Ambiguïtés ({len(r.ambiguities)})\n"
        + "\n".join(f"- {a}" for a in r.ambiguities[:50])
        + "\n\nJSON = source de vérité (`knowledge.json`).\n"
    )
