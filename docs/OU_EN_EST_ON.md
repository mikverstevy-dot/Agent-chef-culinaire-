# Où en est-on — ne pas perdre le travail

Date : 2026-09-27

## Est-ce enregistré ?

**Oui, dans cet espace de travail** : dossier `/home/user/chef-ia/`.

Ce n’est **pas** encore sur GitHub / Supabase / Vercel (aucun compte connecté ici).

Si vous **quittez pour connecter GitHub**, le risque n’est pas que le code « s’auto-détruise » dans le projet, mais qu’une **nouvelle** conversation / sandbox **vide** n’ait pas ce dossier.  
D’où : **pousser sur GitHub dès que le remote existe**, ou télécharger le dossier.

## Ce qui est déjà là (à conserver)

```
chef-ia/
  src/chef_ia/          moteur V0, extraction, fusion, crédits, nutrition, unités
  tests/                16 tests
  data/corpus/          PDF1 Escoffier (~53 Mo) + PDF2–8
  data/extractions/PDF1…PDF8   knowledge.json + rapports
  data/fusion/          fusion_meta.json, fusion_clusters.jsonl, FUSION_RAPPORT.md
  docs/
```

~120 Mo au total.

## Ce qui n’est PAS fini

Pas de K scientifique validée, pas de graphe, pas d’app en ligne, pas de recettes justifiées.

## Pour finir (ordre)

1. **Sauvegarder hors sandbox** : GitHub (`git remote` + `git push`) ou zip téléchargé.
2. **Valider** un échantillon d’extraction (style P1), au moins PDF4/PDF6/PDF5 — ou confirmer le waiver `A_VERIFIER` pour tout.
3. **Décider** : PDF7/PDF8 Bookey hors noyau ? PDF2 = extrait seulement ?
4. **Typer** des atomes (ENTITE, TRANSFORMATION, …) **sans** inventer.
5. Graphe + contradictions **explicites**.
6. Supabase (schéma aligné sur atomes **réels**).
7. Brancher le moteur V0 sur K typée.
8. Interface V1 simple.
9. Vercel + crédits (prix non figés) + week-end gratuit.

Tant que 1 n’est pas fait, ne comptez pas sur « l’IA s’en souviendra ».
