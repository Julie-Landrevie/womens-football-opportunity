# Étape 3 — Résultats chiffrés (FA WSL 2023/24)

Généré par `src/analyze_rankings.py`. Percentiles au sein du groupe de postes, gardiennes exclues. Data: StatsBomb.

## A. Changements de classement (saison complète)

| Seuil | Indicateur | Passage | ρ de Spearman | Bougent ≥ 20 pts | Lien avec la possession |
|---|---|---|---|---|---|
| 900 min (n = 141) | xG hors penalties | total → par 90 | 0.97 | 14 (10%) | +0.10 |
| 900 min (n = 141) | xG hors penalties | par 90 → par possession | 0.98 | 7 (5%) | -0.65 |
| 900 min (n = 141) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.13 |
| 900 min (n = 141) | xA | total → par 90 | 0.96 | 12 (8%) | +0.10 |
| 900 min (n = 141) | xA | par 90 → par possession | 0.98 | 7 (5%) | -0.62 |
| 900 min (n = 141) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.14 |
| 900 min (n = 141) | actions progressives | total → par 90 | 0.86 | 26 (18%) | +0.17 |
| 900 min (n = 141) | actions progressives | par 90 → par possession | 0.95 | 12 (8%) | -0.67 |
| 900 min (n = 141) | actions progressives | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.06 |
| 900 min (n = 141) | pressions | total → par 90 | 0.79 | 64 (45%) | -0.04 |
| 900 min (n = 141) | pressions | par 90 → par possession | 0.88 | 45 (32%) | +0.81 |
| 900 min (n = 141) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.04 |
| 900 min (n = 141) | ballons gagnés | total → par 90 | 0.67 | 68 (48%) | +0.15 |
| 900 min (n = 141) | ballons gagnés | par 90 → par possession | 0.86 | 41 (29%) | +0.70 |
| 900 min (n = 141) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.04 |
| 5 matchs de 60 min (n = 182) | xG hors penalties | total → par 90 | 0.95 | 32 (18%) | +0.12 |
| 5 matchs de 60 min (n = 182) | xG hors penalties | par 90 → par possession | 0.98 | 8 (4%) | -0.67 |
| 5 matchs de 60 min (n = 182) | xG hors penalties | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.08 |
| 5 matchs de 60 min (n = 182) | xA | total → par 90 | 0.93 | 28 (15%) | +0.08 |
| 5 matchs de 60 min (n = 182) | xA | par 90 → par possession | 0.98 | 6 (3%) | -0.66 |
| 5 matchs de 60 min (n = 182) | xA | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.11 |
| 5 matchs de 60 min (n = 182) | actions progressives | total → par 90 | 0.78 | 55 (30%) | +0.20 |
| 5 matchs de 60 min (n = 182) | actions progressives | par 90 → par possession | 0.95 | 14 (8%) | -0.67 |
| 5 matchs de 60 min (n = 182) | actions progressives | par 90 → ajusté adversaire | 1.00 | 0 (0%) | -0.01 |
| 5 matchs de 60 min (n = 182) | pressions | total → par 90 | 0.64 | 90 (50%) | -0.20 |
| 5 matchs de 60 min (n = 182) | pressions | par 90 → par possession | 0.89 | 58 (32%) | +0.79 |
| 5 matchs de 60 min (n = 182) | pressions | par 90 → ajusté adversaire | 1.00 | 0 (0%) | +0.03 |
| 5 matchs de 60 min (n = 182) | ballons gagnés | total → par 90 | 0.54 | 99 (54%) | +0.06 |
| 5 matchs de 60 min (n = 182) | ballons gagnés | par 90 → par possession | 0.86 | 60 (33%) | +0.72 |
| 5 matchs de 60 min (n = 182) | ballons gagnés | par 90 → ajusté adversaire | 1.00 | 1 (0%) | +0.00 |

Plus grands déplacements, par 90 → par possession (seuil 5 matchs de 60 min) :

| Indicateur | Joueuse | Équipe | Poste | Possession | Percentile par 90 | Percentile par possession |
|---|---|---|---|---|---|---|
| xG hors penalties | Chloe Kelly | Manchester City WFC | W | 64% | 65 | 35 |
| xG hors penalties | Leila Ouahabi | Manchester City WFC | FB | 63% | 71 | 44 |
| xG hors penalties | Amalie Thestrup | Bristol City WFC | FW | 33% | 26 | 52 |
| xA | Tatiana Pinto | Brighton & Hove Albion WFC | AM | 44% | 14 | 57 |
| xA | Kim Little | Arsenal WFC | AM | 61% | 57 | 29 |
| xA | Amalie Thestrup | Bristol City WFC | FW | 33% | 22 | 48 |
| actions progressives | Jamie-Lee Napier | Bristol City WFC | FB | 32% | 38 | 85 |
| actions progressives | Ffion Morgan | Bristol City WFC | W | 33% | 16 | 58 |
| actions progressives | Carrie Jones | Bristol City WFC | DM | 32% | 18 | 57 |
| pressions | Ffion Morgan | Bristol City WFC | W | 33% | 65 | 3 |
| pressions | Drew Spence | Tottenham Hotspur Women | AM | 53% | 71 | 14 |
| pressions | Ella Powell | Bristol City WFC | FB | 32% | 59 | 9 |
| ballons gagnés | Tatiana Pinto | Brighton & Hove Albion WFC | AM | 44% | 71 | 14 |
| ballons gagnés | Abigail Harrison | Bristol City WFC | FW | 33% | 96 | 43 |
| ballons gagnés | Hinata Miyazawa | Manchester United W | CM | 60% | 47 | 93 |

## B. Remplaçantes et faible temps de jeu

Part des joueuses de chaque tranche dans le top 10 % du par 90 de leur poste (attendu : 10 %) :

| Indicateur | < 450 min | 450-900 min | ≥ 900 min |
|---|---|---|---|
| xG hors penalties | 14% (n = 77) | 10% (n = 58) | 11% (n = 141) |
| xA | 12% (n = 77) | 9% (n = 58) | 13% (n = 141) |
| actions progressives | 16% (n = 77) | 5% (n = 58) | 12% (n = 141) |
| pressions | 22% (n = 77) | 5% (n = 58) | 8% (n = 141) |
| ballons gagnés | 22% (n = 77) | 9% (n = 58) | 7% (n = 141) |

Mêmes joueuses, titulaires ou entrées en jeu (au moins 3 matchs de chaque) ; valeurs par 90 (part de possession : sans unité), ratio global entrée / titulaire et IC 95 % par bootstrap sur les joueuses :

| Indicateur | Joueuses | Titulaire | Entrée | Ratio entrée / titulaire [IC 95 %] |
|---|---|---|---|---|
| xG hors penalties | 114 | 0.127 | 0.194 | 1.52 [1.18-1.99] |
| xA | 114 | 0.112 | 0.12 | 1.07 [0.82-1.38] |
| actions progressives | 114 | 4.144 | 4.687 | 1.13 [1.0-1.29] |
| pressions | 114 | 17.777 | 19.86 | 1.12 [1.04-1.2] |
| ballons gagnés | 114 | 6.178 | 6.786 | 1.1 [1.02-1.18] |
| ball receipts | 114 | 40.722 | 41.021 | 1.01 [0.96-1.05] |
| part possession equipe | 114 | 0.518 | 0.511 | 0.99 [0.96-1.02] |

Contrôle « fin de match » : les mêmes joueuses, quand elles sont titulaires et jouent tout le match, avant et après la 65e minute (par 90) :

| Indicateur | Matchs complets | Avant la 65e | Après la 65e | Ratio fin / avant |
|---|---|---|---|---|
| xG hors penalties | 444 | 0.099 | 0.1 | 1.01 |
| xA | 444 | 0.106 | 0.086 | 0.82 |
| actions progressives | 444 | 4.239 | 4.038 | 0.95 |
| pressions | 444 | 16.635 | 13.929 | 0.84 |
| ballons gagnés | 444 | 6.253 | 6.399 | 1.02 |

## C. Stabilité (joueuses de champ avec au moins 450 min dans chaque moitié)

ρ de Spearman entre les deux moitiés [IC 95 %] ; « poste » = même calcul sur les percentiles au sein du poste ; entre parenthèses, IC 95 % apparié de l'écart avec le par 90 au sein du poste.

| Découpage | Indicateur | Par 90 | Par possession | Ajusté adversaire |
|---|---|---|---|---|
| aller / retour (n = 103) | xG hors penalties | 0.79 [0.68-0.86] · poste 0.50 | 0.78 [0.67-0.86] · poste 0.48 (écart -0.09 à +0.05) | 0.78 [0.68-0.86] · poste 0.51 (écart -0.03 à +0.06) |
| aller / retour (n = 103) | xA | 0.72 [0.60-0.80] · poste 0.43 | 0.67 [0.54-0.77] · poste 0.37 (écart -0.15 à +0.03) | 0.73 [0.63-0.80] · poste 0.48 (écart +0.01 à +0.11) |
| aller / retour (n = 103) | actions progressives | 0.83 [0.74-0.89] · poste 0.69 | 0.79 [0.68-0.86] · poste 0.58 (écart -0.22 à +0.00) | 0.84 [0.75-0.90] · poste 0.70 (écart -0.04 à +0.06) |
| aller / retour (n = 103) | pressions | 0.90 [0.85-0.94] · poste 0.79 | 0.86 [0.78-0.91] · poste 0.69 (écart -0.21 à -0.00) | 0.90 [0.84-0.93] · poste 0.78 (écart -0.04 à +0.03) |
| aller / retour (n = 103) | ballons gagnés | 0.63 [0.49-0.75] · poste 0.51 | 0.74 [0.62-0.82] · poste 0.67 (écart +0.05 à +0.27) | 0.63 [0.49-0.75] · poste 0.53 (écart -0.01 à +0.07) |
| matchs impairs / pairs (n = 134) | xG hors penalties | 0.76 [0.66-0.82] · poste 0.57 | 0.74 [0.65-0.82] · poste 0.46 (écart -0.18 à -0.04) | 0.76 [0.67-0.83] · poste 0.59 (écart -0.02 à +0.08) |
| matchs impairs / pairs (n = 134) | xA | 0.66 [0.53-0.75] · poste 0.36 | 0.64 [0.52-0.74] · poste 0.29 (écart -0.14 à -0.03) | 0.67 [0.56-0.76] · poste 0.38 (écart -0.02 à +0.06) |
| matchs impairs / pairs (n = 134) | actions progressives | 0.82 [0.74-0.87] · poste 0.69 | 0.80 [0.72-0.86] · poste 0.58 (écart -0.19 à -0.02) | 0.86 [0.80-0.91] · poste 0.75 (écart +0.01 à +0.11) |
| matchs impairs / pairs (n = 134) | pressions | 0.90 [0.84-0.93] · poste 0.74 | 0.89 [0.83-0.92] · poste 0.69 (écart -0.15 à +0.04) | 0.89 [0.84-0.93] · poste 0.76 (écart -0.03 à +0.08) |
| matchs impairs / pairs (n = 134) | ballons gagnés | 0.76 [0.67-0.82] · poste 0.56 | 0.77 [0.68-0.83] · poste 0.62 (écart -0.06 à +0.16) | 0.75 [0.67-0.82] · poste 0.56 (écart -0.05 à +0.03) |

## D. Ajustement à l'adversaire sur une demi-saison

| Moitié | Groupe | Indicateur | Écart max adj / par 90 | Écart médian | Bougent ≥ 20 pts |
|---|---|---|---|---|---|
| aller (11 adversaires) | ≥ 450 min (n = 143) | xG hors penalties | 32% | 3.5% | 0 |
| aller (11 adversaires) | ≥ 450 min (n = 143) | xA | 33% | 4.1% | 0 |
| aller (11 adversaires) | ≥ 450 min (n = 143) | actions progressives | 26% | 2.3% | 2 |
| aller (11 adversaires) | ≥ 450 min (n = 143) | pressions | 6% | 1.1% | 2 |
| aller (11 adversaires) | ≥ 450 min (n = 143) | ballons gagnés | 4% | 0.7% | 0 |
| aller (11 adversaires) | ≥ 3 matchs, < 450 min (n = 70) | xG hors penalties | 65% | 9.2% | 3 |
| aller (11 adversaires) | ≥ 3 matchs, < 450 min (n = 70) | xA | 45% | 11.0% | 1 |
| aller (11 adversaires) | ≥ 3 matchs, < 450 min (n = 70) | actions progressives | 47% | 8.3% | 2 |
| aller (11 adversaires) | ≥ 3 matchs, < 450 min (n = 70) | pressions | 14% | 2.5% | 0 |
| aller (11 adversaires) | ≥ 3 matchs, < 450 min (n = 70) | ballons gagnés | 8% | 1.7% | 0 |
| retour (11 adversaires) | ≥ 450 min (n = 138) | xG hors penalties | 18% | 3.1% | 0 |
| retour (11 adversaires) | ≥ 450 min (n = 138) | xA | 26% | 3.5% | 0 |
| retour (11 adversaires) | ≥ 450 min (n = 138) | actions progressives | 19% | 2.8% | 0 |
| retour (11 adversaires) | ≥ 450 min (n = 138) | pressions | 7% | 1.2% | 0 |
| retour (11 adversaires) | ≥ 450 min (n = 138) | ballons gagnés | 4% | 0.8% | 0 |
| retour (11 adversaires) | ≥ 3 matchs, < 450 min (n = 76) | xG hors penalties | 35% | 9.6% | 0 |
| retour (11 adversaires) | ≥ 3 matchs, < 450 min (n = 76) | xA | 28% | 9.3% | 0 |
| retour (11 adversaires) | ≥ 3 matchs, < 450 min (n = 76) | actions progressives | 28% | 8.9% | 9 |
| retour (11 adversaires) | ≥ 3 matchs, < 450 min (n = 76) | pressions | 14% | 3.3% | 3 |
| retour (11 adversaires) | ≥ 3 matchs, < 450 min (n = 76) | ballons gagnés | 8% | 1.8% | 0 |
