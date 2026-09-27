# PHASE 0 — Audit

Date : 2026-09-27

## Dépôt

- Workspace Arena : **vide** à l’arrivée (aucun GitHub cloné).
- Credentials GitHub / Vercel / Supabase : **absents**.
- Corpus des 6 PDF scientifiques : **absent**.
- Seul fichier fourni : `PROMPT_FINAL_LMARENA_CHEF_IA.pdf` (cahier des charges, 4 pages).

## Conséquence

Conformément à « ne suppose jamais que le dépôt est vide » : il **était** vide. Rien à conserver.

PHASE 2–5 et 6/14 sont **bloquées** tant que corpus et accès ne sont pas fournis.

## Décisions d’implémentation (nécessaires, pas optionnelles)

1. Socle Python local versionné dans `chef-ia/` pour ne pas perdre l’architecture.
2. Statuts épistémiques comme type unique — pas de « score de confiance inventé ».
3. Fusion refusée si < 6 documents validés.
4. Moteur V0 glouton borné ; pas de solveur mathématique V3.
5. Crédits : unités relatives, **prix non figés**.
6. Extraction PDF = spans sourcés, `accepted=False` jusqu’à revue humaine (P1 100/100 était un audit, pas une vérité auto).

## Prochaine étape

Fournir les 6 PDF du corpus (un par un). Extraction séquentielle PDF1 → validation → PDF2 → …
