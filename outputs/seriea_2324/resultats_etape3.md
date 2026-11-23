# Étape 3 — Résultats chiffrés (Serie A Women 2023/24)

Généré par `src/analyze_rankings.py`. Percentiles au sein du groupe de postes, gardiennes exclues. Data: StatsBomb.

## A. Changements de classement (saison complète)

| Seuil | Indicateur | Passage | ρ de Spearman | Bougent ≥ 20 pts | Lien avec la possession |
|---|---|---|---|---|---|
| 900 min (n = 131) | xG hors penalties | total → par 90 | 0.97 | 15 (12%) | +0.16 |
| 900 min (n = 131) | xG hors penalties | par 90 → par possession | 0.99 | 4 (3%) | -0.52 |
| 900 min (n = 131) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.28 |
| 900 min (n = 131) | xA | total → par 90 | 0.95 | 7 (5%) | +0.13 |
| 900 min (n = 131) | xA | par 90 → par possession | 0.98 | 7 (5%) | -0.61 |
| 900 min (n = 131) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.24 |
| 900 min (n = 131) | actions progressives | total → par 90 | 0.87 | 30 (23%) | +0.34 |
| 900 min (n = 131) | actions progressives | par 90 → par possession | 0.94 | 21 (16%) | -0.67 |
| 900 min (n = 131) | actions progressives | par 90 → ajusté adversaire | 0.99 | 1 (1%) | +0.21 |
| 900 min (n = 131) | pressions | total → par 90 | 0.70 | 59 (45%) | +0.04 |
| 900 min (n = 131) | pressions | par 90 → par possession | 0.92 | 33 (25%) | +0.79 |
| 900 min (n = 131) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.34 |
| 900 min (n = 131) | ballons gagnés | total → par 90 | 0.77 | 54 (41%) | +0.10 |
| 900 min (n = 131) | ballons gagnés | par 90 → par possession | 0.91 | 32 (24%) | +0.73 |
| 900 min (n = 131) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.02 |
| 5 matchs de 60 min (n = 160) | xG hors penalties | total → par 90 | 0.95 | 28 (18%) | +0.19 |
| 5 matchs de 60 min (n = 160) | xG hors penalties | par 90 → par possession | 0.99 | 3 (2%) | -0.55 |
| 5 matchs de 60 min (n = 160) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.22 |
| 5 matchs de 60 min (n = 160) | xA | total → par 90 | 0.91 | 31 (19%) | +0.15 |
| 5 matchs de 60 min (n = 160) | xA | par 90 → par possession | 0.98 | 9 (6%) | -0.66 |
| 5 matchs de 60 min (n = 160) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.26 |
| 5 matchs de 60 min (n = 160) | actions progressives | total → par 90 | 0.78 | 57 (36%) | +0.37 |
| 5 matchs de 60 min (n = 160) | actions progressives | par 90 → par possession | 0.94 | 22 (14%) | -0.69 |
| 5 matchs de 60 min (n = 160) | actions progressives | par 90 → ajusté adversaire | 0.99 | 2 (1%) | +0.16 |
| 5 matchs de 60 min (n = 160) | pressions | total → par 90 | 0.58 | 88 (55%) | +0.03 |
| 5 matchs de 60 min (n = 160) | pressions | par 90 → par possession | 0.92 | 43 (27%) | +0.80 |
| 5 matchs de 60 min (n = 160) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.32 |
| 5 matchs de 60 min (n = 160) | ballons gagnés | total → par 90 | 0.63 | 75 (47%) | +0.14 |
| 5 matchs de 60 min (n = 160) | ballons gagnés | par 90 → par possession | 0.91 | 45 (28%) | +0.73 |
| 5 matchs de 60 min (n = 160) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.01 |

Plus grands déplacements, par 90 → par possession (seuil 5 matchs de 60 min) :

| Indicateur | Joueuse | Équipe | Poste | Possession | Percentile par 90 | Percentile par possession |
|---|---|---|---|---|---|---|
| xG hors penalties | Sara Caiazzo | Pomigliano | CB | 40% | 47 | 70 |
| xG hors penalties | Alice Corelli | Napoli W | W | 43% | 43 | 65 |
| xG hors penalties | Elisa del Estal | Napoli W | FW | 43% | 54 | 75 |
| xA | Valentina Giacinti | AS Roma W | FW | 61% | 83 | 42 |
| xA | Laura Bourgouin | Pomigliano | FW | 39% | 42 | 71 |
| xA | Nora Heroum | Sampdoria W | FB | 39% | 33 | 61 |
| actions progressives | Alice Corelli | Napoli W | W | 43% | 30 | 78 |
| actions progressives | Gina-Maria Chmielinski | Napoli W | AM | 42% | 38 | 75 |
| actions progressives | G.Giacobbo | Napoli W | W | 41% | 17 | 52 |
| pressions | Evelyn Ijeh | AC Milan W | FW | 54% | 33 | 79 |
| pressions | Taty | Sampdoria W | FW | 39% | 58 | 12 |
| pressions | Eseosa Aigbogun | AS Roma W | FB | 66% | 53 | 92 |
| ballons gagnés | Saki Kumagai | AS Roma W | DM | 60% | 42 | 79 |
| ballons gagnés | Eseosa Aigbogun | AS Roma W | FB | 66% | 56 | 89 |
| ballons gagnés | Iris Madeleine Rabot | Pomigliano | CM | 41% | 60 | 27 |

## B. Remplaçantes et faible temps de jeu

Part des joueuses de chaque tranche dans le top 10 % du par 90 de leur poste (attendu : 10 %) :

| Indicateur | < 450 min | 450-900 min | ≥ 900 min |
|---|---|---|---|
| xG hors penalties | 11% (n = 70) | 9% (n = 44) | 12% (n = 131) |
| xA | 14% (n = 70) | 7% (n = 44) | 11% (n = 131) |
| actions progressives | 19% (n = 70) | 7% (n = 44) | 8% (n = 131) |
| pressions | 20% (n = 70) | 7% (n = 44) | 8% (n = 131) |
| ballons gagnés | 14% (n = 70) | 9% (n = 44) | 10% (n = 131) |

Mêmes joueuses, titulaires ou entrées en jeu (au moins 3 matchs de chaque) ; valeurs par 90 (part de possession : sans unité), ratio global entrée / titulaire et IC 95 % par bootstrap sur les joueuses :

| Indicateur | Joueuses | Titulaire | Entrée | Ratio entrée / titulaire [IC 95 %] |
|---|---|---|---|---|
| xG hors penalties | 110 | 0.154 | 0.202 | 1.31 [1.06-1.6] |
| xA | 110 | 0.093 | 0.121 | 1.3 [1.04-1.6] |
| actions progressives | 110 | 3.906 | 4.466 | 1.14 [1.02-1.28] |
| pressions | 110 | 16.528 | 17.725 | 1.07 [1.01-1.14] |
| ballons gagnés | 110 | 6.267 | 6.844 | 1.09 [1.02-1.16] |
| ball receipts | 110 | 38.974 | 39.448 | 1.01 [0.97-1.06] |
| part possession equipe | 110 | 0.509 | 0.507 | 1.0 [0.97-1.02] |

Contrôle « fin de match » : les mêmes joueuses, quand elles sont titulaires et jouent tout le match, avant et après la 65e minute (par 90) :

| Indicateur | Matchs complets | Avant la 65e | Après la 65e | Ratio fin / avant |
|---|---|---|---|---|
| xG hors penalties | 456 | 0.121 | 0.15 | 1.24 |
| xA | 456 | 0.081 | 0.096 | 1.18 |
| actions progressives | 456 | 3.871 | 3.784 | 0.98 |
| pressions | 456 | 15.989 | 13.507 | 0.84 |
| ballons gagnés | 456 | 6.308 | 5.847 | 0.93 |

## C. Stabilité (joueuses de champ avec au moins 450 min dans chaque moitié)

ρ de Spearman entre les deux moitiés [IC 95 %] ; « poste » = même calcul sur les percentiles au sein du poste ; entre parenthèses, IC 95 % apparié de l'écart avec le par 90 au sein du poste.

| Découpage | Indicateur | Par 90 | Par possession | Ajusté adversaire |
|---|---|---|---|---|
| 1re phase / reste (n = 85) | xG hors penalties | 0.86 [0.78-0.91] · poste 0.72 | 0.84 [0.76-0.89] · poste 0.60 (écart -0.22 à -0.05) | 0.86 [0.79-0.91] · poste 0.74 (écart -0.02 à +0.06) |
| 1re phase / reste (n = 85) | xA | 0.67 [0.52-0.77] · poste 0.49 | 0.61 [0.46-0.73] · poste 0.37 (écart -0.21 à -0.05) | 0.67 [0.53-0.78] · poste 0.50 (écart -0.04 à +0.05) |
| 1re phase / reste (n = 85) | actions progressives | 0.77 [0.65-0.86] · poste 0.72 | 0.76 [0.65-0.84] · poste 0.57 (écart -0.25 à -0.06) | 0.80 [0.68-0.87] · poste 0.72 (écart -0.05 à +0.06) |
| 1re phase / reste (n = 85) | pressions | 0.85 [0.77-0.91] · poste 0.79 | 0.85 [0.78-0.90] · poste 0.79 (écart -0.08 à +0.08) | 0.84 [0.76-0.90] · poste 0.77 (écart -0.06 à +0.03) |
| 1re phase / reste (n = 85) | ballons gagnés | 0.86 [0.79-0.91] · poste 0.70 | 0.85 [0.76-0.90] · poste 0.69 (écart -0.14 à +0.10) | 0.87 [0.80-0.91] · poste 0.70 (écart -0.04 à +0.03) |
| matchs impairs / pairs (n = 122) | xG hors penalties | 0.86 [0.81-0.90] · poste 0.65 | 0.85 [0.80-0.89] · poste 0.56 (écart -0.14 à -0.03) | 0.87 [0.81-0.91] · poste 0.66 (écart -0.02 à +0.06) |
| matchs impairs / pairs (n = 122) | xA | 0.59 [0.44-0.72] · poste 0.40 | 0.54 [0.40-0.68] · poste 0.31 (écart -0.17 à -0.02) | 0.61 [0.48-0.73] · poste 0.44 (écart -0.01 à +0.09) |
| matchs impairs / pairs (n = 122) | actions progressives | 0.86 [0.81-0.90] · poste 0.76 | 0.85 [0.80-0.89] · poste 0.74 (écart -0.09 à +0.06) | 0.88 [0.82-0.92] · poste 0.81 (écart +0.01 à +0.11) |
| matchs impairs / pairs (n = 122) | pressions | 0.89 [0.83-0.92] · poste 0.74 | 0.85 [0.79-0.90] · poste 0.68 (écart -0.15 à +0.03) | 0.89 [0.84-0.93] · poste 0.72 (écart -0.05 à +0.02) |
| matchs impairs / pairs (n = 122) | ballons gagnés | 0.82 [0.74-0.88] · poste 0.68 | 0.76 [0.66-0.85] · poste 0.71 (écart -0.07 à +0.13) | 0.83 [0.76-0.89] · poste 0.70 (écart +0.00 à +0.05) |

## D. Ajustement à l'adversaire sur une demi-saison

| Moitié | Groupe | Indicateur | Écart max adj / par 90 | Écart médian | Bougent ≥ 20 pts |
|---|---|---|---|---|---|
| 1re phase (9 adversaires) | ≥ 450 min (n = 98) | xG hors penalties | 25% | 5.0% | 0 |
| 1re phase (9 adversaires) | ≥ 450 min (n = 98) | xA | 23% | 4.9% | 0 |
| 1re phase (9 adversaires) | ≥ 450 min (n = 98) | actions progressives | 18% | 2.9% | 0 |
| 1re phase (9 adversaires) | ≥ 450 min (n = 98) | pressions | 6% | 1.2% | 0 |
| 1re phase (9 adversaires) | ≥ 450 min (n = 98) | ballons gagnés | 3% | 0.7% | 0 |
| 1re phase (9 adversaires) | ≥ 3 matchs, < 450 min (n = 78) | xG hors penalties | 32% | 9.3% | 2 |
| 1re phase (9 adversaires) | ≥ 3 matchs, < 450 min (n = 78) | xA | 39% | 9.4% | 1 |
| 1re phase (9 adversaires) | ≥ 3 matchs, < 450 min (n = 78) | actions progressives | 28% | 7.1% | 4 |
| 1re phase (9 adversaires) | ≥ 3 matchs, < 450 min (n = 78) | pressions | 10% | 2.8% | 1 |
| 1re phase (9 adversaires) | ≥ 3 matchs, < 450 min (n = 78) | ballons gagnés | 8% | 1.8% | 0 |
| reste de la saison (9 adversaires) | ≥ 450 min (n = 148) | xG hors penalties | 14% | 5.5% | 1 |
| reste de la saison (9 adversaires) | ≥ 450 min (n = 148) | xA | 18% | 5.0% | 1 |
| reste de la saison (9 adversaires) | ≥ 450 min (n = 148) | actions progressives | 18% | 6.3% | 2 |
| reste de la saison (9 adversaires) | ≥ 450 min (n = 148) | pressions | 7% | 3.0% | 0 |
| reste de la saison (9 adversaires) | ≥ 450 min (n = 148) | ballons gagnés | 4% | 0.8% | 0 |
| reste de la saison (9 adversaires) | ≥ 3 matchs, < 450 min (n = 46) | xG hors penalties | 31% | 8.5% | 0 |
| reste de la saison (9 adversaires) | ≥ 3 matchs, < 450 min (n = 46) | xA | 28% | 7.7% | 0 |
| reste de la saison (9 adversaires) | ≥ 3 matchs, < 450 min (n = 46) | actions progressives | 30% | 7.7% | 4 |
| reste de la saison (9 adversaires) | ≥ 3 matchs, < 450 min (n = 46) | pressions | 9% | 3.7% | 0 |
| reste de la saison (9 adversaires) | ≥ 3 matchs, < 450 min (n = 46) | ballons gagnés | 4% | 1.3% | 0 |
