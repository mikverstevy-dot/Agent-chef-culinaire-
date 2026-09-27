"""CLI minimale V0."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from chef_ia.credits import estimate
from chef_ia.engine import CulinaryEngine, parse_user_intent
from chef_ia.extraction.pipeline import extract_document, save_extraction
from chef_ia.knowledge import KnowledgeBase


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="chef-ia")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--query", required=True, help='ex: "ingredients: oeuf, farine | forbid: arachide"')

    e = sub.add_parser("extract")
    e.add_argument("pdf")
    e.add_argument("--id", required=True)
    e.add_argument("--out", required=True)

    a = p.parse_args(argv)

    if a.cmd == "extract":
        items, report = extract_document(a.pdf, a.id)
        save_extraction(Path(a.out), items, report)
        print(json.dumps({"n": report.n_elements, "accepted": report.accepted, "out": a.out}, ensure_ascii=False))
        return 0

    if a.cmd == "generate":
        r0, c = parse_user_intent(a.query)
        kb = KnowledgeBase()  # corpus vide jusqu'aux PDF validés
        eng = CulinaryEngine(kb)
        cred = estimate(
            n_hard=len(c.hard),
            n_soft=len(c.soft),
            n_ingredients=len(r0.entities),
            n_knowledge=0,
            n_steps=0,
            nutrition=False,
            external_search=False,
            now=datetime.now(timezone.utc),
        )
        print(cred.message)
        res = eng.generate(r0, c)
        print(json.dumps(res.as_dict(), ensure_ascii=False, indent=2))
        return 0 if res.ok else 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
