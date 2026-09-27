"""Fusion uniquement après validation des six extraits. Pas de moyenne de conflits."""

from __future__ import annotations

from chef_ia.knowledge import Conflict, KnowledgeAtom, KnowledgeBase


class FusionError(RuntimeError):
    pass


def fuse(validated_atoms: list[KnowledgeAtom], n_documents_required: int = 6) -> KnowledgeBase:
    docs = {a.trace.document_id for a in validated_atoms}
    if len(docs) < n_documents_required:
        raise FusionError(
            f"fusion interdite: {len(docs)} document(s) validé(s) < {n_documents_required}"
        )
    kb = KnowledgeBase()
    seen_hash: dict[str, str] = {}
    for a in validated_atoms:
        key = (a.original_wording or str(a.content)).strip().lower()
        if key in seen_hash:
            # complémentarité de provenance — on conserve les deux ids distincts
            pass
        seen_hash[key] = a.id
        kb.add(a)
    return kb


def register_conflict(kb: KnowledgeBase, a_id: str, b_id: str, description: str) -> None:
    cid = f"conflict-{a_id}-{b_id}"
    kb.conflicts[cid] = Conflict(id=cid, atom_ids=[a_id, b_id], description=description)
