# Inventaire corpus — extractions individuelles

Date : 2026-09-27  
Règle : **pas de fusion** tant que chaque extrait n’est pas validé.  
Tous : `accepted = false`.

Le cahier des charges parlait de **6** PDF. L’utilisateur a fourni **8 fichiers + Escoffier déjà extrait**. Un fichier est un **doublon**.

| ID | Document réel | Pages | Spans | Nature épistémique du *document* | Validé |
|---|---|---|---|---|---|
| PDF1 | Escoffier, *Guide culinaire*, 1907 (IA b21525730) | 818 | 28918 | Original historique | NON |
| — | `guide_culinaire_compresse.pdf` | 818 | — | **DOUBLON PDF1** — non ré-extrait | — |
| PDF2 | Gilles Charles, *La Cuisine expliquée*, extrait BPI réf. 2070 | 27 | 2041 | **Extrait commercial**, pas l’ouvrage complet | NON |
| PDF3 | Collège Paul Langevin, *Ramène ta science en cuisine !*, CGEN 2018 | 34 | 672 | Atelier collège / vulgarisation scolaire | NON |
| PDF4 | PNNS, *La santé vient en mangeant — guide alimentaire pour tous* | 65 | 4959 | Guide nutrition santé (institutionnel FR) | NON |
| PDF5 | *La cuisine moléculaire* (doc 22 p.) | 22 | 533 | Document court ; attributions à contrôler (ex. « Nicholas Curtis » vs Kurti — **non corrigé** dans K) | NON |
| PDF6 | PAM/WFP, *Manuel de l’alimentation et de la nutrition*, déc. 2018 | 185 | 7109 | Manuel institutionnel nutrition | NON |
| PDF7 | Bookey — résumé *On Food and Cooking* (McGee) | 40 | 722 | **Résumé tiers**, pas McGee original → spans = EXPLICITE *de Bookey* | NON |
| PDF8 | Bookey — résumé Wolke *What Einstein told his cook* | 122 | 1864 | **Résumé tiers**, pas Wolke original | NON |

**Total spans extraits (PDF1–8, hors doublon) : 46 818**

## Ce qui n’a PAS été fait (volontairement)

- fusion, déduplication inter-documents, graphe, Internet
- promotion d’un résumé Bookey au rang de McGee/Wolke `EXPLICITE`
- correction silencieuse d’erreurs de source
- acceptation automatique type score 100/100

## Décisions nécessitant validation

1. Le corpus « 6 PDF » du master prompt ≠ ces 8 fichiers. Faut-il **restreindre** à 6, et lesquels ?
2. PDF7/PDF8 Bookey : **exclure** du noyau scientifique, ou garder comme `EXTERNE` seulement ?
3. PDF2 n’est qu’un extrait : K ne doit pas prétendre couvrir *La Cuisine expliquée* entier.
4. PDF1 Escoffier : volume historique vs physique contemporaine — ne pas homogénéiser.

## Prochaine étape protocole

Validation humaine **par document**, dans l’ordre PDF1 → PDF8.  
Puis seulement fusion.
