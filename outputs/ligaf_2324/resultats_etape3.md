# Étape 3 — Résultats chiffrés (Liga F 2023/24)

Généré par `src/analyze_rankings.py`. Percentiles au sein du groupe de postes, gardiennes exclues. Data: StatsBomb.

## A. Changements de classement (saison complète)

| Seuil | Indicateur | Passage | ρ de Spearman | Bougent ≥ 20 pts | Lien avec la possession |
|---|---|---|---|---|---|
| 900 min (n = 228) | xG hors penalties | total → par 90 | 0.97 | 25 (11%) | +0.10 |
| 900 min (n = 228) | xG hors penalties | par 90 → par possession | 0.98 | 8 (4%) | -0.71 |
| 900 min (n = 228) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.19 |
| 900 min (n = 228) | xA | total → par 90 | 0.96 | 17 (8%) | +0.26 |
| 900 min (n = 228) | xA | par 90 → par possession | 0.98 | 19 (8%) | -0.68 |
| 900 min (n = 228) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.09 |
| 900 min (n = 228) | actions progressives | total → par 90 | 0.87 | 51 (22%) | +0.28 |
| 900 min (n = 228) | actions progressives | par 90 → par possession | 0.92 | 39 (17%) | -0.72 |
| 900 min (n = 228) | actions progressives | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.07 |
| 900 min (n = 228) | pressions | total → par 90 | 0.72 | 106 (46%) | -0.01 |
| 900 min (n = 228) | pressions | par 90 → par possession | 0.87 | 82 (36%) | +0.86 |
| 900 min (n = 228) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.07 |
| 900 min (n = 228) | ballons gagnés | total → par 90 | 0.69 | 97 (42%) | +0.13 |
| 900 min (n = 228) | ballons gagnés | par 90 → par possession | 0.85 | 63 (28%) | +0.80 |
| 900 min (n = 228) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.14 |
| 5 matchs de 60 min (n = 252) | xG hors penalties | total → par 90 | 0.95 | 33 (13%) | +0.14 |
| 5 matchs de 60 min (n = 252) | xG hors penalties | par 90 → par possession | 0.98 | 9 (4%) | -0.73 |
| 5 matchs de 60 min (n = 252) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.10 |
| 5 matchs de 60 min (n = 252) | xA | total → par 90 | 0.94 | 28 (11%) | +0.27 |
| 5 matchs de 60 min (n = 252) | xA | par 90 → par possession | 0.98 | 15 (6%) | -0.68 |
| 5 matchs de 60 min (n = 252) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.08 |
| 5 matchs de 60 min (n = 252) | actions progressives | total → par 90 | 0.82 | 65 (26%) | +0.31 |
| 5 matchs de 60 min (n = 252) | actions progressives | par 90 → par possession | 0.93 | 36 (14%) | -0.74 |
| 5 matchs de 60 min (n = 252) | actions progressives | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.01 |
| 5 matchs de 60 min (n = 252) | pressions | total → par 90 | 0.66 | 128 (51%) | -0.06 |
| 5 matchs de 60 min (n = 252) | pressions | par 90 → par possession | 0.86 | 91 (36%) | +0.85 |
| 5 matchs de 60 min (n = 252) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.11 |
| 5 matchs de 60 min (n = 252) | ballons gagnés | total → par 90 | 0.63 | 112 (44%) | +0.12 |
| 5 matchs de 60 min (n = 252) | ballons gagnés | par 90 → par possession | 0.83 | 71 (28%) | +0.79 |
| 5 matchs de 60 min (n = 252) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.19 |

Plus grands déplacements, par 90 → par possession (seuil 5 matchs de 60 min) :

| Indicateur | Joueuse | Équipe | Poste | Possession | Percentile par 90 | Percentile par possession |
|---|---|---|---|---|---|---|
| xG hors penalties | Mariona Caldentey | Barcelona WFC | FW | 70% | 62 | 32 |
| xG hors penalties | Keira Walsh | Barcelona WFC | DM | 72% | 46 | 21 |
| xG hors penalties | Irene Paredes | Barcelona WFC | CB | 69% | 81 | 56 |
| xA | Andrea Sierra | SD Eibar | FB | 37% | 37 | 67 |
| xA | Amanda Sampedro | Sevilla FC | AM | 50% | 57 | 86 |
| xA | Natasa Andonova | Levante UD Femenino | AM | 64% | 86 | 57 |
| actions progressives | Bruna Vilamala | Barcelona WFC | W | 70% | 71 | 24 |
| actions progressives | Annelie Leitner | SD Eibar | FB | 35% | 35 | 80 |
| actions progressives | Miku Kojima | CD Sporting de Huelva | DM | 32% | 23 | 67 |
| pressions | Patri Guijarro | Barcelona WFC | DM | 69% | 21 | 95 |
| pressions | Bruna Vilamala | Barcelona WFC | W | 70% | 20 | 80 |
| pressions | Amanda Sampedro | Sevilla FC | AM | 50% | 86 | 29 |
| ballons gagnés | Keira Walsh | Barcelona WFC | DM | 72% | 13 | 82 |
| ballons gagnés | Fridolina Rolfö | Barcelona WFC | FB | 74% | 4 | 69 |
| ballons gagnés | Claudia Pina | Barcelona WFC | W | 70% | 20 | 83 |

## B. Remplaçantes et faible temps de jeu

Part des joueuses de chaque tranche dans le top 10 % du par 90 de leur poste (attendu : 10 %) :

| Indicateur | < 450 min | 450-900 min | ≥ 900 min |
|---|---|---|---|
| xG hors penalties | 11% (n = 99) | 10% (n = 39) | 10% (n = 228) |
| xA | 9% (n = 99) | 3% (n = 39) | 13% (n = 228) |
| actions progressives | 9% (n = 99) | 8% (n = 39) | 12% (n = 228) |
| pressions | 21% (n = 99) | 8% (n = 39) | 7% (n = 228) |
| ballons gagnés | 17% (n = 99) | 8% (n = 39) | 8% (n = 228) |

Mêmes joueuses, titulaires ou entrées en jeu (au moins 3 matchs de chaque) ; valeurs par 90 (part de possession : sans unité), ratio global entrée / titulaire et IC 95 % par bootstrap sur les joueuses :

| Indicateur | Joueuses | Titulaire | Entrée | Ratio entrée / titulaire [IC 95 %] |
|---|---|---|---|---|
| xG hors penalties | 208 | 0.133 | 0.183 | 1.37 [1.17-1.61] |
| xA | 208 | 0.097 | 0.122 | 1.26 [1.07-1.46] |
| actions progressives | 208 | 3.672 | 4.198 | 1.14 [1.03-1.26] |
| pressions | 208 | 17.606 | 19.329 | 1.1 [1.05-1.14] |
| ballons gagnés | 208 | 6.449 | 6.818 | 1.06 [1.01-1.11] |
| ball receipts | 208 | 41.272 | 41.491 | 1.01 [0.96-1.04] |
| part possession equipe | 208 | 0.511 | 0.512 | 1.0 [0.98-1.03] |

Contrôle « fin de match » : les mêmes joueuses, quand elles sont titulaires et jouent tout le match, avant et après la 65e minute (par 90) :

| Indicateur | Matchs complets | Avant la 65e | Après la 65e | Ratio fin / avant |
|---|---|---|---|---|
| xG hors penalties | 1382 | 0.111 | 0.121 | 1.09 |
| xA | 1382 | 0.096 | 0.104 | 1.08 |
| actions progressives | 1382 | 3.748 | 3.658 | 0.98 |
| pressions | 1382 | 16.638 | 14.223 | 0.85 |
| ballons gagnés | 1382 | 6.437 | 6.459 | 1.0 |

## C. Stabilité (joueuses de champ avec au moins 450 min dans chaque moitié)

ρ de Spearman entre les deux moitiés [IC 95 %] ; « poste » = même calcul sur les percentiles au sein du poste ; entre parenthèses, IC 95 % apparié de l'écart avec le par 90 au sein du poste.

| Découpage | Indicateur | Par 90 | Par possession | Ajusté adversaire |
|---|---|---|---|---|
| 1re phase / reste (n = 199) | xG hors penalties | 0.77 [0.70-0.83] · poste 0.54 | 0.75 [0.67-0.81] · poste 0.46 (écart -0.13 à -0.03) | 0.77 [0.68-0.83] · poste 0.54 (écart -0.01 à +0.02) |
| 1re phase / reste (n = 199) | xA | 0.64 [0.55-0.72] · poste 0.42 | 0.59 [0.49-0.67] · poste 0.33 (écart -0.14 à -0.04) | 0.64 [0.53-0.73] · poste 0.43 (écart -0.00 à +0.03) |
| 1re phase / reste (n = 199) | actions progressives | 0.83 [0.77-0.87] · poste 0.72 | 0.77 [0.70-0.82] · poste 0.57 (écart -0.21 à -0.09) | 0.83 [0.77-0.87] · poste 0.72 (écart -0.02 à +0.02) |
| 1re phase / reste (n = 199) | pressions | 0.84 [0.78-0.88] · poste 0.71 | 0.85 [0.79-0.89] · poste 0.69 (écart -0.10 à +0.05) | 0.84 [0.78-0.88] · poste 0.69 (écart -0.04 à +0.01) |
| 1re phase / reste (n = 199) | ballons gagnés | 0.80 [0.73-0.85] · poste 0.67 | 0.81 [0.74-0.86] · poste 0.74 (écart -0.01 à +0.14) | 0.79 [0.72-0.84] · poste 0.67 (écart -0.02 à +0.02) |
| matchs impairs / pairs (n = 223) | xG hors penalties | 0.79 [0.71-0.84] · poste 0.54 | 0.78 [0.71-0.82] · poste 0.48 (écart -0.12 à -0.01) | 0.79 [0.72-0.84] · poste 0.55 (écart -0.01 à +0.03) |
| matchs impairs / pairs (n = 223) | xA | 0.69 [0.61-0.76] · poste 0.43 | 0.64 [0.55-0.71] · poste 0.36 (écart -0.11 à -0.02) | 0.69 [0.61-0.75] · poste 0.46 (écart -0.00 à +0.05) |
| matchs impairs / pairs (n = 223) | actions progressives | 0.86 [0.82-0.90] · poste 0.80 | 0.84 [0.79-0.88] · poste 0.69 (écart -0.16 à -0.06) | 0.88 [0.83-0.91] · poste 0.80 (écart -0.02 à +0.03) |
| matchs impairs / pairs (n = 223) | pressions | 0.88 [0.84-0.91] · poste 0.72 | 0.91 [0.88-0.93] · poste 0.78 (écart -0.00 à +0.12) | 0.90 [0.86-0.92] · poste 0.74 (écart +0.01 à +0.06) |
| matchs impairs / pairs (n = 223) | ballons gagnés | 0.78 [0.72-0.82] · poste 0.64 | 0.78 [0.71-0.83] · poste 0.67 (écart -0.06 à +0.11) | 0.78 [0.71-0.83] · poste 0.65 (écart -0.01 à +0.03) |

## D. Ajustement à l'adversaire sur une demi-saison

| Moitié | Groupe | Indicateur | Écart max adj / par 90 | Écart médian | Bougent ≥ 20 pts |
|---|---|---|---|---|---|
| 1re phase (15 adversaires) | ≥ 450 min (n = 224) | xG hors penalties | 28% | 3.8% | 0 |
| 1re phase (15 adversaires) | ≥ 450 min (n = 224) | xA | 37% | 4.1% | 0 |
| 1re phase (15 adversaires) | ≥ 450 min (n = 224) | actions progressives | 21% | 2.9% | 0 |
| 1re phase (15 adversaires) | ≥ 450 min (n = 224) | pressions | 8% | 1.6% | 0 |
| 1re phase (15 adversaires) | ≥ 450 min (n = 224) | ballons gagnés | 5% | 0.7% | 0 |
| 1re phase (15 adversaires) | ≥ 3 matchs, < 450 min (n = 68) | xG hors penalties | 26% | 6.9% | 0 |
| 1re phase (15 adversaires) | ≥ 3 matchs, < 450 min (n = 68) | xA | 46% | 10.6% | 1 |
| 1re phase (15 adversaires) | ≥ 3 matchs, < 450 min (n = 68) | actions progressives | 28% | 6.8% | 2 |
| 1re phase (15 adversaires) | ≥ 3 matchs, < 450 min (n = 68) | pressions | 19% | 4.6% | 3 |
| 1re phase (15 adversaires) | ≥ 3 matchs, < 450 min (n = 68) | ballons gagnés | 5% | 1.9% | 0 |
| reste de la saison (15 adversaires) | ≥ 450 min (n = 231) | xG hors penalties | 22% | 2.9% | 0 |
| reste de la saison (15 adversaires) | ≥ 450 min (n = 231) | xA | 23% | 2.9% | 0 |
| reste de la saison (15 adversaires) | ≥ 450 min (n = 231) | actions progressives | 18% | 2.8% | 0 |
| reste de la saison (15 adversaires) | ≥ 450 min (n = 231) | pressions | 7% | 1.7% | 0 |
| reste de la saison (15 adversaires) | ≥ 450 min (n = 231) | ballons gagnés | 6% | 0.8% | 0 |
| reste de la saison (15 adversaires) | ≥ 3 matchs, < 450 min (n = 64) | xG hors penalties | 128% | 9.1% | 0 |
| reste de la saison (15 adversaires) | ≥ 3 matchs, < 450 min (n = 64) | xA | 116% | 9.0% | 4 |
| reste de la saison (15 adversaires) | ≥ 3 matchs, < 450 min (n = 64) | actions progressives | 97% | 7.3% | 2 |
| reste de la saison (15 adversaires) | ≥ 3 matchs, < 450 min (n = 64) | pressions | 18% | 4.7% | 10 |
| reste de la saison (15 adversaires) | ≥ 3 matchs, < 450 min (n = 64) | ballons gagnés | 13% | 2.5% | 3 |
