# CHEF IA — Moteur culinaire scientifique

Vision : une IA qui comprend **pourquoi** une recette fonctionne et peut en créer une nouvelle **à partir de contraintes**.

Ce n’est **pas** un chatbot de recettes générique.

## Priorités

1. Intégrité scientifique  
2. Traçabilité  
3. Absence d’invention  
4. Cohérence des données  
5. Robustesse du moteur  
6. Tests  
7. Simplicité de l’interface  
8. Performance  
9. Monétisation  

Une fonction commerciale ne doit jamais dégrader l’intégrité scientifique.

## Statuts épistémiques (obligatoires)

| Statut | Sens |
|---|---|
| `EXPLICITE` | Directement présent dans une source |
| `DEDUIT` | Déduction logique justifiable, prémisses conservées |
| `APPROXIME_EMPIRIQUE` | Approximation / tendance de la source |
| `A_VERIFIER` | Insuffisamment établi |
| `EXTERNE` | Source Internet / externe, traçable |

Valeur inconnue → `UNKNOWN`. Jamais inventée.

## Phases

| Phase | Statut local |
|---|---|
| 0 Audit dépôt | Terminée (workspace vide, pas de GitHub/Supabase) |
| 1 Pipeline PDF | Squelette + schéma + tests |
| 2–4 Corpus 6 PDF | **Bloqué** : corpus non fourni |
| 5 Internet | Après fusion |
| 6 Supabase | Après schéma validé sur données réelles |
| 7–9 Moteur V0 | Modèle d’états + contraintes + anti-invention |
| 10–11 Crédits / week-end | Modèle configurable, prix non figés |
| 12 Interface | Non prioritaire tant que K est vide |
| 13 Tests | A–O partiels (sans corpus) |
| 14 GitHub + Vercel | Credentials absents |

## Lancer

```bash
cd chef-ia
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m pytest tests -q
PYTHONPATH=src python3 -m chef_ia.cli --help
```

## Règle d’or

Si une information indispensable manque : **connaissances disponibles insuffisantes** — jamais d’invention.
