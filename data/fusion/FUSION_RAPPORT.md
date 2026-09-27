# PHASE 4 — Fusion (entamée, non close)

**Waiver opérateur 2026-09-27** : fusion sans acceptation préalable des extraits.  
Statut du **jeu fusionné** : `A_VERIFIER`.  
Aucune moyenne, aucune loi `EXPLICITE` nouvelle, aucun graphe causal auto.

## Volumes

| | |
|---|---|
| Spans en entrée (PDF1–8) | 46 818 |
| Clusters (libellé normalisé) | 44 976 |
| Libellés présents dans **plusieurs** documents | **44** (souvent formules / bruit, pas des lois) |
| Clusters touchant un résumé Bookey | 2 409 |
| Doublon Escoffier compressé | exclu |

Déduplication = **même phrase**, provenances empilées.  
Ce n’est **pas** « ces deux phrases parlent du même phénomène donc une règle ».

## Tensions documentaires (non tranchées)

1. Escoffier 1907 vs PNNS / PAM 2002–2018 (nutrition, sel, sécurité).
2. Bookey ≠ McGee / Wolke originaux.
3. PDF2 = extrait incomplet.
4. PDF5 : attributions source conservées telles quelles.

Pas de « vérité unique » choisie.

## Trous (réels, pas hypothèses scientifiques)

- Pas d’ontologie typée (`ENTITE`, `TRANSFORMATION`, …).
- Pas de graphe ingrédient → effet.
- Pas de conversion SI des seuils.
- Tableaux nutritionnels non atomisés.
- Contradictions **numériques** non détectées auto (risque d’inventer des conflits OCR).

## Fichiers

- `fusion_meta.json` — compteurs, tensions, trous
- `fusion_clusters.jsonl` — 1 cluster / ligne, `epistemologie_fusion: A_VERIFIER`

## Ce qui reste interdit

Enrichissement Internet, chargement Supabase comme faits, génération de recettes « scientifiques » à partir de ces clusters.

## Prochaine étape (protocole)

Revue / typage d’un **échantillon** (style P1) **ou** PHASE 5 Internet **seulement** sur lacunes listées, données `EXTERNE`.
