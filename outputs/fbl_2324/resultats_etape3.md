# Étape 3 — Résultats chiffrés (Frauen-Bundesliga 2023/24)

Généré par `src/analyze_rankings.py`. Percentiles au sein du groupe de postes, gardiennes exclues. Data: StatsBomb.

## A. Changements de classement (saison complète)

| Seuil | Indicateur | Passage | ρ de Spearman | Bougent ≥ 20 pts | Lien avec la possession |
|---|---|---|---|---|---|
| 900 min (n = 134) | xG hors penalties | total → par 90 | 0.98 | 13 (10%) | +0.03 |
| 900 min (n = 134) | xG hors penalties | par 90 → par possession | 0.99 | 5 (4%) | -0.64 |
| 900 min (n = 134) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.12 |
| 900 min (n = 134) | xA | total → par 90 | 0.98 | 3 (2%) | +0.20 |
| 900 min (n = 134) | xA | par 90 → par possession | 0.99 | 4 (3%) | -0.59 |
| 900 min (n = 134) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.04 |
| 900 min (n = 134) | actions progressives | total → par 90 | 0.91 | 27 (20%) | +0.20 |
| 900 min (n = 134) | actions progressives | par 90 → par possession | 0.95 | 8 (6%) | -0.59 |
| 900 min (n = 134) | actions progressives | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.15 |
| 900 min (n = 134) | pressions | total → par 90 | 0.76 | 63 (47%) | -0.11 |
| 900 min (n = 134) | pressions | par 90 → par possession | 0.81 | 51 (38%) | +0.87 |
| 900 min (n = 134) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.13 |
| 900 min (n = 134) | ballons gagnés | total → par 90 | 0.79 | 40 (30%) | +0.17 |
| 900 min (n = 134) | ballons gagnés | par 90 → par possession | 0.86 | 33 (25%) | +0.71 |
| 900 min (n = 134) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 1 (1%) | -0.08 |
| 5 matchs de 60 min (n = 174) | xG hors penalties | total → par 90 | 0.95 | 26 (15%) | +0.09 |
| 5 matchs de 60 min (n = 174) | xG hors penalties | par 90 → par possession | 0.99 | 4 (2%) | -0.60 |
| 5 matchs de 60 min (n = 174) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.09 |
| 5 matchs de 60 min (n = 174) | xA | total → par 90 | 0.95 | 16 (9%) | +0.09 |
| 5 matchs de 60 min (n = 174) | xA | par 90 → par possession | 0.99 | 5 (3%) | -0.62 |
| 5 matchs de 60 min (n = 174) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.00 |
| 5 matchs de 60 min (n = 174) | actions progressives | total → par 90 | 0.84 | 47 (27%) | +0.21 |
| 5 matchs de 60 min (n = 174) | actions progressives | par 90 → par possession | 0.95 | 12 (7%) | -0.62 |
| 5 matchs de 60 min (n = 174) | actions progressives | par 90 → ajusté adversaire | 1.00 | 1 (1%) | +0.10 |
| 5 matchs de 60 min (n = 174) | pressions | total → par 90 | 0.56 | 87 (50%) | -0.26 |
| 5 matchs de 60 min (n = 174) | pressions | par 90 → par possession | 0.82 | 63 (36%) | +0.88 |
| 5 matchs de 60 min (n = 174) | pressions | par 90 → ajusté adversaire | 1.00 | 2 (1%) | +0.02 |
| 5 matchs de 60 min (n = 174) | ballons gagnés | total → par 90 | 0.67 | 70 (40%) | +0.02 |
| 5 matchs de 60 min (n = 174) | ballons gagnés | par 90 → par possession | 0.86 | 35 (20%) | +0.74 |
| 5 matchs de 60 min (n = 174) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 1 (1%) | -0.07 |

Plus grands déplacements, par 90 → par possession (seuil 5 matchs de 60 min) :

| Indicateur | Joueuse | Équipe | Poste | Possession | Percentile par 90 | Percentile par possession |
|---|---|---|---|---|---|---|
| xG hors penalties | Sarah Freutel | Duisburg WFC | FB | 35% | 65 | 88 |
| xG hors penalties | Amira Arfaoui | Nürnberg W | AM | 38% | 33 | 56 |
| xG hors penalties | Lina Magull | Bayern München W | W | 61% | 85 | 63 |
| xA | Lisa Josten | Duisburg WFC | FW | 37% | 52 | 80 |
| xA | Medina Desic | Nürnberg W | FW | 39% | 48 | 72 |
| xA | Amira Arfaoui | Nürnberg W | AM | 38% | 33 | 56 |
| actions progressives | Madeleine Steck | Nürnberg W | CB | 38% | 54 | 82 |
| actions progressives | Lea Schüller | Bayern München W | FW | 62% | 36 | 8 |
| actions progressives | Amira Arfaoui | Nürnberg W | AM | 38% | 67 | 89 |
| pressions | Miray Cin | Duisburg WFC | CM | 35% | 100 | 27 |
| pressions | Antonia-Johanna Halverkamps | Duisburg WFC | W | 35% | 96 | 26 |
| pressions | Kerstin Bogenschütz | Nürnberg W | AM | 37% | 89 | 22 |
| ballons gagnés | Alexandria Loy Hess | Duisburg WFC | FW | 36% | 84 | 28 |
| ballons gagnés | Jelena Prvulovic | Duisburg WFC | FW | 37% | 72 | 20 |
| ballons gagnés | Kara Bathmann | Duisburg WFC | FB | 35% | 85 | 33 |

## B. Remplaçantes et faible temps de jeu

Part des joueuses de chaque tranche dans le top 10 % du par 90 de leur poste (attendu : 10 %) :

| Indicateur | < 450 min | 450-900 min | ≥ 900 min |
|---|---|---|---|
| xG hors penalties | 16% (n = 81) | 6% (n = 55) | 10% (n = 134) |
| xA | 10% (n = 81) | 9% (n = 55) | 13% (n = 134) |
| actions progressives | 12% (n = 81) | 4% (n = 55) | 13% (n = 134) |
| pressions | 24% (n = 81) | 13% (n = 55) | 3% (n = 134) |
| ballons gagnés | 18% (n = 81) | 7% (n = 55) | 8% (n = 134) |

Mêmes joueuses, titulaires ou entrées en jeu (au moins 3 matchs de chaque) ; valeurs par 90 (part de possession : sans unité), ratio global entrée / titulaire et IC 95 % par bootstrap sur les joueuses :

| Indicateur | Joueuses | Titulaire | Entrée | Ratio entrée / titulaire [IC 95 %] |
|---|---|---|---|---|
| xG hors penalties | 105 | 0.141 | 0.188 | 1.33 [1.0-1.77] |
| xA | 105 | 0.083 | 0.107 | 1.28 [0.93-1.79] |
| actions progressives | 105 | 3.227 | 3.694 | 1.14 [1.02-1.27] |
| pressions | 105 | 18.967 | 19.317 | 1.02 [0.96-1.08] |
| ballons gagnés | 105 | 6.905 | 7.147 | 1.03 [0.96-1.12] |
| ball receipts | 105 | 38.164 | 38.248 | 1.0 [0.95-1.05] |
| part possession equipe | 105 | 0.499 | 0.508 | 1.02 [0.99-1.05] |

Contrôle « fin de match » : les mêmes joueuses, quand elles sont titulaires et jouent tout le match, avant et après la 65e minute (par 90) :

| Indicateur | Matchs complets | Avant la 65e | Après la 65e | Ratio fin / avant |
|---|---|---|---|---|
| xG hors penalties | 356 | 0.101 | 0.129 | 1.27 |
| xA | 356 | 0.078 | 0.08 | 1.04 |
| actions progressives | 356 | 3.141 | 3.427 | 1.09 |
| pressions | 356 | 18.238 | 15.127 | 0.83 |
| ballons gagnés | 356 | 7.207 | 7.196 | 1.0 |

## C. Stabilité (joueuses de champ avec au moins 450 min dans chaque moitié)

ρ de Spearman entre les deux moitiés [IC 95 %] ; « poste » = même calcul sur les percentiles au sein du poste ; entre parenthèses, IC 95 % apparié de l'écart avec le par 90 au sein du poste.

| Découpage | Indicateur | Par 90 | Par possession | Ajusté adversaire |
|---|---|---|---|---|
| 1re phase / reste (n = 108) | xG hors penalties | 0.75 [0.63-0.83] · poste 0.59 | 0.72 [0.59-0.81] · poste 0.50 (écart -0.15 à -0.02) | 0.74 [0.61-0.82] · poste 0.58 (écart -0.04 à +0.03) |
| 1re phase / reste (n = 108) | xA | 0.60 [0.46-0.71] · poste 0.42 | 0.54 [0.40-0.67] · poste 0.33 (écart -0.18 à -0.00) | 0.60 [0.47-0.71] · poste 0.42 (écart -0.04 à +0.05) |
| 1re phase / reste (n = 108) | actions progressives | 0.80 [0.71-0.86] · poste 0.72 | 0.70 [0.58-0.80] · poste 0.56 (écart -0.27 à -0.07) | 0.81 [0.73-0.87] · poste 0.75 (écart +0.00 à +0.06) |
| 1re phase / reste (n = 108) | pressions | 0.81 [0.71-0.89] · poste 0.77 | 0.81 [0.72-0.88] · poste 0.70 (écart -0.19 à +0.04) | 0.81 [0.71-0.88] · poste 0.76 (écart -0.04 à +0.03) |
| 1re phase / reste (n = 108) | ballons gagnés | 0.72 [0.59-0.80] · poste 0.60 | 0.77 [0.67-0.83] · poste 0.62 (écart -0.11 à +0.14) | 0.72 [0.59-0.80] · poste 0.62 (écart -0.03 à +0.06) |
| matchs impairs / pairs (n = 128) | xG hors penalties | 0.78 [0.69-0.84] · poste 0.53 | 0.76 [0.68-0.82] · poste 0.49 (écart -0.11 à +0.01) | 0.78 [0.69-0.84] · poste 0.53 (écart -0.04 à +0.04) |
| matchs impairs / pairs (n = 128) | xA | 0.69 [0.59-0.79] · poste 0.49 | 0.66 [0.54-0.76] · poste 0.44 (écart -0.11 à +0.00) | 0.71 [0.60-0.80] · poste 0.52 (écart -0.02 à +0.07) |
| matchs impairs / pairs (n = 128) | actions progressives | 0.87 [0.81-0.91] · poste 0.80 | 0.84 [0.78-0.89] · poste 0.76 (écart -0.12 à +0.02) | 0.89 [0.83-0.92] · poste 0.84 (écart -0.00 à +0.09) |
| matchs impairs / pairs (n = 128) | pressions | 0.88 [0.82-0.92] · poste 0.74 | 0.91 [0.86-0.93] · poste 0.76 (écart -0.09 à +0.12) | 0.90 [0.84-0.93] · poste 0.76 (écart -0.01 à +0.06) |
| matchs impairs / pairs (n = 128) | ballons gagnés | 0.77 [0.68-0.83] · poste 0.68 | 0.79 [0.71-0.84] · poste 0.71 (écart -0.06 à +0.12) | 0.77 [0.67-0.84] · poste 0.69 (écart -0.02 à +0.04) |

## D. Ajustement à l'adversaire sur une demi-saison

| Moitié | Groupe | Indicateur | Écart max adj / par 90 | Écart médian | Bougent ≥ 20 pts |
|---|---|---|---|---|---|
| 1re phase (11 adversaires) | ≥ 450 min (n = 135) | xG hors penalties | 39% | 4.1% | 0 |
| 1re phase (11 adversaires) | ≥ 450 min (n = 135) | xA | 40% | 5.6% | 0 |
| 1re phase (11 adversaires) | ≥ 450 min (n = 135) | actions progressives | 27% | 2.9% | 0 |
| 1re phase (11 adversaires) | ≥ 450 min (n = 135) | pressions | 6% | 1.2% | 1 |
| 1re phase (11 adversaires) | ≥ 450 min (n = 135) | ballons gagnés | 6% | 0.9% | 0 |
| 1re phase (11 adversaires) | ≥ 3 matchs, < 450 min (n = 77) | xG hors penalties | 37% | 15.0% | 0 |
| 1re phase (11 adversaires) | ≥ 3 matchs, < 450 min (n = 77) | xA | 66% | 14.6% | 3 |
| 1re phase (11 adversaires) | ≥ 3 matchs, < 450 min (n = 77) | actions progressives | 42% | 9.7% | 2 |
| 1re phase (11 adversaires) | ≥ 3 matchs, < 450 min (n = 77) | pressions | 15% | 3.8% | 0 |
| 1re phase (11 adversaires) | ≥ 3 matchs, < 450 min (n = 77) | ballons gagnés | 10% | 2.5% | 0 |
| reste de la saison (11 adversaires) | ≥ 450 min (n = 140) | xG hors penalties | 24% | 3.7% | 0 |
| reste de la saison (11 adversaires) | ≥ 450 min (n = 140) | xA | 33% | 4.7% | 0 |
| reste de la saison (11 adversaires) | ≥ 450 min (n = 140) | actions progressives | 15% | 2.5% | 0 |
| reste de la saison (11 adversaires) | ≥ 450 min (n = 140) | pressions | 6% | 1.3% | 0 |
| reste de la saison (11 adversaires) | ≥ 450 min (n = 140) | ballons gagnés | 4% | 1.3% | 0 |
| reste de la saison (11 adversaires) | ≥ 3 matchs, < 450 min (n = 72) | xG hors penalties | 46% | 9.0% | 0 |
| reste de la saison (11 adversaires) | ≥ 3 matchs, < 450 min (n = 72) | xA | 52% | 9.6% | 2 |
| reste de la saison (11 adversaires) | ≥ 3 matchs, < 450 min (n = 72) | actions progressives | 32% | 8.0% | 2 |
| reste de la saison (11 adversaires) | ≥ 3 matchs, < 450 min (n = 72) | pressions | 20% | 4.2% | 3 |
| reste de la saison (11 adversaires) | ≥ 3 matchs, < 450 min (n = 72) | ballons gagnés | 9% | 2.0% | 3 |
