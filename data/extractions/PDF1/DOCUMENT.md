# PDF1 — identité (ne pas fusionner)

| Champ | Valeur | Statut |
|---|---|---|
| id interne | `PDF1_ESCOFFIER_1907` | — |
| Titre | Le Guide culinaire, aide-mémoire de cuisine pratique | EXPLICITE (notice IA) |
| Auteur principal | Escoffier, A. (Auguste), 1846–1935 | EXPLICITE (notice IA) |
| Autres | Gilbert, Philéas ; Fetu, Emile | EXPLICITE (notice IA) |
| Date publication | 1907 | EXPLICITE (notice IA) |
| Éditeur | Paris : Colin | EXPLICITE (notice IA) |
| Langue | français | EXPLICITE (notice IA) |
| Collection | University of Leeds Library / Blanche Leigh / COOKERY 8-ESC | EXPLICITE (page de garde + notice) |
| Identifiant Leeds barcode | 3 0106 01103 5705 | EXPLICITE (couverture utilisateur) |
| Identifiant IA | `b21525730` | EXTERNE (catalogue) |
| URL | https://archive.org/details/b21525730 | EXTERNE |
| Fichier local | `data/corpus/PDF1_b21525730.pdf` (≈53 Mo, 818 pages PDF) | — |
| Consulté | 2026-09-27 | — |

## Nature du document

Manuel culinaire professionnel historique (1907).  
Ce n’est **pas** un traité de physico-chimie alimentaire moderne.

Conséquence pour K :

- Les recettes et formulations d’Escoffier, **si revues**, peuvent devenir `EXPLICITE` **du corpus Escoffier 1907**, pas des lois physiques.
- Températures, durées, « fonds », techniques : conserver le **libellé source** ; ne pas convertir en seuils SI inventés.
- OCR (ex. `jjour`, `cjue`) → ambiguïté, pas correction silencieuse présentée comme EXPLICITE du livre.

## Pipeline

Extraction **individuelle** terminée.  
`accepted = false` jusqu’à validation humaine (règle §18 / test P1).  
**Pas de fusion.** PDF2 non commencé.
