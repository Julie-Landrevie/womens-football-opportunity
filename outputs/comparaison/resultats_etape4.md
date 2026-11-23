# Étape 4 — Comparaison des quatre championnats féminins 2023/24

Généré par `src/compare_leagues.py`. Joueuses de champ avec au moins 5 matchs de 60 min ; percentiles au sein du groupe de postes. Data: StatsBomb.

## 1. Contexte

| Ligue | Équipes | Matchs | Joueuses | Possession / match | Possession des équipes | Buts / match | xG hors pen. / match | Entrées en jeu / match |
|---|---|---|---|---|---|---|---|---|
| FA WSL | 12 | 132 | 296 | 57.0 min | 33% à 63% | 3.31 | 2.84 | 8.2 |
| Frauen-Bundesliga | 12 | 132 | 294 | 52.7 min | 35% à 63% | 3.2 | 2.61 | 8.7 |
| Liga F | 16 | 240 | 400 | 53.5 min | 36% à 70% | 3.15 | 2.55 | 8.7 |
| Serie A Women | 10 | 130 | 259 | 52.4 min | 40% à 60% | 3.12 | 2.56 | 8.4 |

## 2. Du par 90 au par possession : part des joueuses qui bougent d'au moins 20 points

| Indicateur | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women | 4 ligues réunies |
|---|---|---|---|---|---|
| xG hors penalties | 4% (-0.67) | 2% (-0.60) | 4% (-0.73) | 2% (-0.55) | 3% (-0.74) |
| xA | 3% (-0.66) | 3% (-0.62) | 6% (-0.68) | 6% (-0.66) | 3% (-0.74) |
| actions progressives | 8% (-0.67) | 7% (-0.62) | 14% (-0.74) | 14% (-0.69) | 9% (-0.74) |
| pressions | 32% (+0.79) | 36% (+0.88) | 36% (+0.85) | 27% (+0.80) | 34% (+0.88) |
| ballons gagnés | 33% (+0.72) | 20% (+0.74) | 28% (+0.79) | 28% (+0.73) | 26% (+0.80) |

Entre parenthèses : corrélation entre le déplacement et la part de possession de l'équipe.

## 3. Ajustement à l'adversaire

Saison complète, par 90 → ajusté : joueuses qui bougent d'au moins 20 points.

| Indicateur | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women |
|---|---|---|---|---|
| xG hors penalties | 0 | 0 | 0 | 0 |
| xA | 0 | 0 | 0 | 0 |
| actions progressives | 0 | 1 | 0 | 2 |
| pressions | 0 | 2 | 0 | 0 |
| ballons gagnés | 1 | 1 | 0 | 0 |

Par phase (joueuses ≥ 450 min) : écart médian entre ajusté et par 90, et joueuses qui bougent de 20 points.

| Ligue | Phase | Adversaires distincts (min.) | xG hors pen. | Actions progressives | Pressions |
|---|---|---|---|---|---|
| FA WSL | 1re phase | 11 | 3.5% (0) | 2.3% (2) | 1.1% (2) |
| FA WSL | reste de la saison | 11 | 3.1% (0) | 2.8% (0) | 1.2% (0) |
| Frauen-Bundesliga | 1re phase | 11 | 4.1% (0) | 2.9% (0) | 1.2% (1) |
| Frauen-Bundesliga | reste de la saison | 11 | 3.7% (0) | 2.5% (0) | 1.3% (0) |
| Liga F | 1re phase | 15 | 3.8% (0) | 2.9% (0) | 1.6% (0) |
| Liga F | reste de la saison | 15 | 2.9% (0) | 2.8% (0) | 1.7% (0) |
| Serie A Women | 1re phase | 9 | 5.0% (0) | 2.9% (0) | 1.2% (0) |
| Serie A Women | reste de la saison | 9 | 5.5% (1) | 6.3% (2) | 3.0% (0) |

## 4. Entrer en jeu plutôt que commencer

Mêmes joueuses (au moins 3 matchs de chaque), ratio global par 90 entrée / titulaire [IC 95 %] :

| Indicateur | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women |
|---|---|---|---|---|
| xG hors penalties | 1.52 [1.18-1.99] | 1.33 [1.00-1.77] | 1.37 [1.17-1.61] | 1.31 [1.06-1.60] |
| xA | 1.07 [0.82-1.38] | 1.28 [0.93-1.79] | 1.26 [1.07-1.46] | 1.30 [1.04-1.60] |
| actions progressives | 1.13 [1.00-1.29] | 1.14 [1.02-1.27] | 1.14 [1.03-1.26] | 1.14 [1.02-1.28] |
| pressions | 1.12 [1.04-1.20] | 1.02 [0.96-1.08] | 1.10 [1.05-1.14] | 1.07 [1.01-1.14] |
| ballons gagnés | 1.10 [1.02-1.18] | 1.03 [0.96-1.12] | 1.06 [1.01-1.11] | 1.09 [1.02-1.16] |
| ballons reçus | 1.01 [0.96-1.05] | 1.00 [0.95-1.05] | 1.01 [0.96-1.04] | 1.01 [0.97-1.06] |
| part de possession | 0.99 [0.96-1.02] | 1.02 [0.99-1.05] | 1.00 [0.98-1.03] | 1.00 [0.97-1.02] |

Titulaires qui jouent tout le match : ratio par 90 après / avant la 65e minute.

| Indicateur | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women |
|---|---|---|---|---|
| xG hors penalties | 1.01 | 1.27 | 1.09 | 1.24 |
| xA | 0.82 | 1.04 | 1.08 | 1.18 |
| actions progressives | 0.95 | 1.09 | 0.98 | 0.98 |
| pressions | 0.84 | 0.83 | 0.85 | 0.84 |
| ballons gagnés | 1.02 | 1.00 | 1.00 | 0.93 |

**Test « même fenêtre »** : remplaçantes entrées à partir de la 65e minute contre les mêmes joueuses titulaires, sur la même fenêtre (65e → fin du match). Au moins 3 matchs de chaque.

| Périmètre | Joueuses | Indicateur | Titulaire (fenêtre) | Entrée tardive | Ratio [IC 95 %] |
|---|---|---|---|---|---|
| 4 ligues | 200 | xG hors penalties | 0.104 | 0.154 | 1.48 [1.13-1.92] |
| 4 ligues | 200 | xA | 0.07 | 0.103 | 1.48 [1.05-2.09] |
| 4 ligues | 200 | actions progressives | 3.215 | 4.011 | 1.25 [1.10-1.40] |
| 4 ligues | 200 | pressions | 13.722 | 18.272 | 1.33 [1.25-1.42] |
| 4 ligues | 200 | ballons gagnés | 6.536 | 7.135 | 1.09 [1.01-1.18] |
| Frauen-Bundesliga | 29 | xG hors penalties | 0.137 | 0.138 | 1.01 [0.38-2.73] |
| Frauen-Bundesliga | 29 | xA | 0.051 | 0.099 | 1.93 [0.58-4.91] |
| Frauen-Bundesliga | 29 | actions progressives | 3.327 | 3.686 | 1.11 [0.84-1.52] |
| Frauen-Bundesliga | 29 | pressions | 13.982 | 18.055 | 1.29 [1.09-1.51] |
| Frauen-Bundesliga | 29 | ballons gagnés | 7.565 | 7.855 | 1.04 [0.82-1.31] |
| Liga F | 101 | xG hors penalties | 0.089 | 0.157 | 1.76 [1.22-2.51] |
| Liga F | 101 | xA | 0.071 | 0.118 | 1.67 [1.07-2.53] |
| Liga F | 101 | actions progressives | 3.042 | 3.97 | 1.31 [1.09-1.54] |
| Liga F | 101 | pressions | 13.54 | 18.675 | 1.38 [1.27-1.50] |
| Liga F | 101 | ballons gagnés | 6.585 | 7.253 | 1.10 [0.99-1.22] |
| Serie A Women | 44 | xG hors penalties | 0.148 | 0.16 | 1.08 [0.73-1.58] |
| Serie A Women | 44 | xA | 0.058 | 0.092 | 1.59 [0.95-2.55] |
| Serie A Women | 44 | actions progressives | 3.364 | 3.59 | 1.07 [0.84-1.33] |
| Serie A Women | 44 | pressions | 13.913 | 18.057 | 1.30 [1.12-1.50] |
| Serie A Women | 44 | ballons gagnés | 5.595 | 6.682 | 1.19 [1.03-1.38] |
| FA WSL | 26 | xG hors penalties | 0.083 | 0.145 | 1.74 [0.94-3.15] |
| FA WSL | 26 | xA | 0.093 | 0.062 | 0.66 [0.39-1.24] |
| FA WSL | 26 | actions progressives | 3.674 | 5.21 | 1.42 [1.05-1.93] |
| FA WSL | 26 | pressions | 14.036 | 17.159 | 1.22 [0.99-1.50] |
| FA WSL | 26 | ballons gagnés | 6.798 | 6.703 | 0.99 [0.84-1.15] |

## 5. Hiérarchie des ligues : médiane par 90 et par possession (rang entre parenthèses)

| Indicateur | Version | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women |
|---|---|---|---|---|---|
| xG hors penalties | par 90 | 0.077 (1) | 0.075 (2) | 0.066 (4) | 0.075 (3) |
| xG hors penalties | par possession | 0.087 (3) | 0.089 (2) | 0.078 (4) | 0.094 (1) |
| xA | par 90 | 0.067 (1) | 0.053 (4) | 0.061 (3) | 0.064 (2) |
| xA | par possession | 0.082 (2) | 0.066 (4) | 0.082 (3) | 0.087 (1) |
| actions progressives | par 90 | 3.266 (2) | 2.842 (4) | 2.924 (3) | 3.485 (1) |
| actions progressives | par possession | 3.764 (2) | 3.46 (4) | 3.602 (3) | 4.222 (1) |
| pressions | par 90 | 17.167 (2) | 17.447 (1) | 16.476 (3) | 15.136 (4) |
| pressions | par possession | 21.154 (3) | 21.368 (1) | 21.159 (2) | 19.304 (4) |
| ballons gagnés | par 90 | 5.989 (4) | 6.882 (1) | 6.364 (2) | 6.305 (3) |
| ballons gagnés | par possession | 7.199 (4) | 8.313 (1) | 7.928 (2) | 7.884 (3) |

## 6. Stabilité au sein du poste (1re phase contre reste de la saison)

| Indicateur | Version | FA WSL | Frauen-Bundesliga | Liga F | Serie A Women |
|---|---|---|---|---|---|
| xG hors penalties | par 90 | 0.50 | 0.59 | 0.54 | 0.72 |
| xG hors penalties | par possession | 0.48 | 0.50 | 0.46 | 0.60 |
| xA | par 90 | 0.43 | 0.42 | 0.42 | 0.49 |
| xA | par possession | 0.37 | 0.33 | 0.33 | 0.37 |
| actions progressives | par 90 | 0.69 | 0.72 | 0.72 | 0.72 |
| actions progressives | par possession | 0.58 | 0.56 | 0.57 | 0.57 |
| pressions | par 90 | 0.79 | 0.77 | 0.71 | 0.79 |
| pressions | par possession | 0.69 | 0.70 | 0.69 | 0.79 |
| ballons gagnés | par 90 | 0.51 | 0.60 | 0.67 | 0.70 |
| ballons gagnés | par possession | 0.67 | 0.62 | 0.74 | 0.69 |
