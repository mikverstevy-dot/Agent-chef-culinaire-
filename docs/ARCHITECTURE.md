# Architecture V0

```
Entrée → parse_user_intent → C_hard ∪ C_soft, R0
       → estimate crédits (week-end TZ)
       → CulinaryEngine.generate(R0, C, K)
            A(R,K) depuis K utilisable seulement
            T(R,a) avec historique H ordonné (non-commutativité)
            E(R,C) = ∞ si hard violé
            arrêt E≤ε ou Nmax ou INSUFFICIENT_KNOWLEDGE
       → recette + ids de connaissances + incertitudes
```

LLM n’est **pas** branché en V0 : l’intention est un DSL (`ingredients: … | forbid: …`).
Le LLM interviendra en PHASE 7 **derrière** le moteur symbolique, jamais comme source de faits.
