# Rapport de contrôle — extraction PDF1

JSON source de vérité : `knowledge.json`

## Chiffres

| Métrique | Valeur |
|---|---|
| Pages PDF | 818 |
| Pages avec au moins 1 span | 2–817 (page 1 souvent image de garde, texte vide) |
| Éléments extraits | 28 918 |
| EXPLICITE (span source) | 28 815 |
| APPROXIME_EMPIRIQUE (heuristique « vers/environ ») | 103 |
| Doublons d’id | 0 (id hash document+page+ligne) |
| Références orphelines | 0 (chaque span a document_id + page + citation) |
| Accepté | **NON** |
| Score auto type P1 100/100 | **non attribué** (P1 = audit humain 2 pages) |

## Fidélité

- Un span = une ligne OCR ≥ 8 caractères.
- **Aucune** combinaison A+B+C → D.
- **Aucune** température normalisée en seuil exact.
- Formulation source copiée dans `citation` et `original_wording`.

## Anomalies (à vérifier, pas « corrigées »)

1. OCR 1907 : substitutions (`jjour`/`pour`, `cjue`/`que`, `^` pour cédilles, etc.).
2. Pages images (garde Leeds) : peu ou pas de texte.
3. L’heuristique « environ/vers » est **grossière** : 103 lignes marquées APPROXIME_EMPIRIQUE — à revoir page par page, pas une loi.
4. `type_element = AUTRE_TYPE_JUSTIFIE` pour tout le volume : **pas** d’ontologisation automatique (interdit d’inventer ENTITE/REGLE sans revue).
5. Le Guide culinaire mélange recettes, conseils et opinions d’époque : un span EXPLICITE = « le texte dit cela », **pas** « c’est vrai en 2026 ».

## Couverture

Couverture **textuelle des lignes extractibles**, pas couverture scientifique d’un graphe ingrédient→transformation.

Comparaison P1 (2 p., 43 éléments, 100/100) : ce run n’est **pas** équivalent ; volume 818 p. sans revue humaine.

## Décision

Extraction **enregistrée, non validée**.  
Enrichissement de la base opérationnelle K **interdit** tant que ce rapport n’est pas accepté.

Prochaine étape demandée par le protocole : **validation PDF1** puis seulement **PDF2**.
