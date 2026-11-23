# womens-football-opportunity

Mesurer la performance des joueuses **selon les opportunités qu'elles ont eues** (temps de jeu, possession de l'équipe et de l'adversaire, ballons reçus, niveau de l'adversaire), en football féminin, sur StatsBomb Open Data : FA WSL, Frauen-Bundesliga, Liga F et Serie A Women 2023/24.

Idée inspirée de Bozděch (2026, *PLOS ONE*, doi 10.1371/journal.pone.0359538) : mesurer la performance selon les opportunités de l'exprimer. Normalisation par la possession et percentiles par poste inspirés des analyses SkillCorner de Victoria Friss de Kereki.

**Application** : `streamlit run streamlit_app.py` (classements selon la version, fiche joueuse, effet « entrer en jeu », méthode et limites).

## Lancer tout le projet

```bash
pip install -r requirements.txt
python src/download.py all data_raw                         # 634 matchs, ~1,9 Go (non versionnés)
python src/build_player_match.py all data_raw data/processed     # étape 1
python src/build_indicators.py all data_raw data/processed       # étape 2
python src/analyze_rankings.py all data/processed outputs data_raw   # étape 3 (≈ 1 min par ligue)
python src/compare_leagues.py data/processed outputs data_raw        # étape 4
python -m pytest tests
streamlit run streamlit_app.py
```

Chaque script prend en premier argument une ligue (`wsl`, `fbl`, `ligaf`, `seriea`), plusieurs séparées par des virgules, ou `all` (voir `src/leagues.py`). Données brutes dans `data_raw/<ligue>_2324/`, tables dans `data/processed/*_<ligue>_2324.csv`, résultats dans `outputs/<ligue>_2324/` et `outputs/comparaison/`. Bootstrap à graine fixe : les chiffres sont reproductibles.

| Ligue | Clé | Matchs | Joueuses | Contrôles |
|---|---|---|---|---|
| FA WSL | `wsl` | 132 | 296 | 11 titulaires partout ; buts pour = score final à 100 % pour les joueuses qui jouent tout le match ; manques de temps de jeu tous expliqués par une expulsion |
| Frauen-Bundesliga | `fbl` | 132 | 294 | idem |
| Liga F | `ligaf` | 240 | 400 | idem, sauf un match à 0,99 dû à des sorties temporaires pour soins |
| Serie A Women | `seriea` | 130 | 259 | idem ; 18 journées puis deux poules de 5 (calendrier déséquilibré) |

## Étape 1 — Données et table « joueuse × match »

Sortie : `data/processed/player_match_<ligue>_2324.csv`, une ligne par joueuse et par match joué.

### Colonnes
| Colonne | Définition |
|---|---|
| `league` | Clé de la ligue |
| `match_id`, `match_date`, `match_week` | Match |
| `team`, `opponent`, `home`, `team_goals`, `opp_goals` | Équipe, adversaire, domicile, score final |
| `player_id`, `player` | Joueuse (surnom StatsBomb si disponible) |
| `starter` | Titulaire |
| `main_position`, `position_group` | Poste le plus fréquent dans ses événements ; groupe GK, CB, FB, DM, CM, AM, W, FW |
| `seconds_played`, `minutes_played` | Temps sur le terrain, temps additionnel compris |
| `match_seconds` | Durée réelle du match (somme des périodes) |
| `team_possessions_on`, `opp_possessions_on` | Possessions commencées pendant sa présence |
| `team_possession_s_on`, `opp_possession_s_on` | Temps de possession pendant sa présence (du premier événement de jeu de la possession à la fin du dernier) |
| `team_possession_share_on` | Part de possession de l'équipe pendant sa présence |
| `ball_receipts`, `ball_receipts_ok` | Ballons reçus (événements *Ball Receipt*), dont réussis |
| `goals_for_on`, `goals_against_on` | Buts marqués et encaissés par l'équipe pendant sa présence |

### Choix de méthode
- **Temps de jeu reconstruit à partir des événements** (titulaires, remplacements, cartons rouges et seconds jaunes, sorties temporaires *Player Off / Player On*). Les horaires de poste des fichiers de composition sont incohérents dans plusieurs matchs (périodes inversées, joueuses comptées deux fois).
- **Horloge continue** : StatsBomb remet l'horloge à 45:00 en 2e période alors que la 1re peut finir à 47:xx ; tout est converti en temps écoulé réel.
- **Temps de possession** : du premier au dernier événement de jeu de chaque possession. Les arrêts de jeu entre deux possessions ne sont attribués à personne, et les événements administratifs (fin de période, remplacement, blessure, changement tactique, carton hors faute) sont ignorés : sinon ils prolongent la possession en cours pendant l'arrêt (+7,6 min par match en WSL, corrigé à l'étape 3). Résultat : 52 à 57 min par match selon la ligue, contre ≈ 101 min de durée totale. Proche de l'esprit des « 30 min de possession » (TIP / OTIP) de SkillCorner, sans être identique (SkillCorner travaille sur du tracking).

## Étape 2 — Indicateurs et leurs quatre versions

Sorties : `player_match_indicators_<ligue>_2324.csv` (table de l'étape 1 + comptes) et `player_season_versions_<ligue>_2324.csv` (une ligne par joueuse et par équipe ; colonnes `eligible_900` et `eligible_5x60` pour les deux seuils).

| Indicateur | Définition |
|---|---|
| `npxg` | xG hors penalties (modèle StatsBomb) |
| `xa` | xG des tirs qui suivent une passe de la joueuse |
| `prog` | Passes réussies (hors coups de pied arrêtés) et conduites qui partent au-delà des 40 % de son camp et finissent au moins 25 % plus près du but |
| `pressures` | Pressions |
| `ball_wins` | Tacles gagnés + interceptions gagnées + récupérations réussies |

| Version | Calcul |
|---|---|
| `_total` | Somme sur la saison |
| `_p90` | Par 90 minutes jouées |
| `_poss` | Offensifs : par 30 min de possession de l'équipe pendant sa présence ; défensifs : par 30 min de possession adverse (logique TIP / OTIP de SkillCorner) |
| `_adj` | Par 90, ajusté à l'adversaire : total ÷ Σ(minutes/90 × facteur adversaire). Facteur = ce que les équipes produisent contre cet adversaire ÷ moyenne de la ligue, **sans l'équipe de la joueuse** |

Contrôles en WSL : 375 npxG pour 402 buts hors penalties et csc ; xA = 69 % du npxG ; ordres de grandeur par poste cohérents (npxG/90 médian : FW 0,32, CB 0,04) ; facteur adversaire centré sur 1.

## Étape 3 — Classements et stabilité, par ligue

Sorties : 7 tables dans `outputs/<ligue>_2324/tables/` et un résumé chiffré par ligue, par exemple [`outputs/wsl_2324/resultats_etape3.md`](outputs/wsl_2324/resultats_etape3.md). Percentiles calculés **au sein du groupe de postes**, gardiennes exclues. Stabilité : première phase (chaque adversaire affronté une fois) contre reste de la saison, et matchs impairs contre pairs.

### Ce que ça montre en WSL (182 joueuses de champ avec au moins 5 matchs de 60 min ; mêmes conclusions au seuil de 900 min)

1. **Le total mesure surtout le temps de jeu.** Du total au par 90, la moitié des joueuses bougent d'au moins 20 points de percentile pour les pressions (50 %) et les ballons gagnés (54 %), contre 15 à 30 % pour les indicateurs offensifs.
2. **La possession change les classements défensifs, pas offensifs.** Du par 90 au par possession adverse, un tiers des joueuses bougent d'au moins 20 points en pressions (32 %) et en ballons gagnés (33 %), et le déplacement suit la domination de l'équipe (corrélation +0,79 et +0,72 avec la part de possession). Offensif : 3 à 8 % seulement.
3. **L'ajustement à l'adversaire ne change rien**, ni sur une saison, ni sur une phase.
4. **Sans seuil de temps de jeu, les tops par 90 se remplissent de petits temps de jeu.** 22 % des joueuses à moins de 450 min sont dans le top 10 % de leur poste en pressions et en ballons gagnés (attendu : 10 %).
5. **Une joueuse qui entre en jeu produit plus par 90 que la même joueuse titulaire** (114 joueuses, au moins 3 matchs de chaque) : pressions ×1,12 [IC 95 % 1,04-1,20], ballons gagnés ×1,10, actions progressives ×1,13, xG hors penalties ×1,52 ; part de possession de l'équipe identique. Voir l'étape 4 pour le test sur la même fenêtre de match.
6. **Stabilité** : les pressions sont l'indicateur le plus stable (ρ = 0,90). Au sein du poste, la version par possession est plus stable pour les ballons gagnés, moins stable pour les autres indicateurs. Une version moins stable n'est pas une moins bonne mesure : le par 90 garde une part de « style d'équipe » qui ne change pas d'une moitié à l'autre.

## Étape 4 — Quatre championnats

Résumé : [`outputs/comparaison/resultats_etape4.md`](outputs/comparaison/resultats_etape4.md). Table commune pour l'application : `data/processed/player_season_versions_all_2324.csv`.

1. **La possession déplace un tiers des joueuses en défense, dans les quatre ligues** : du par 90 au par possession adverse, 27 à 36 % bougent d'au moins 20 points en pressions, 20 à 33 % en ballons gagnés, toujours en suivant la domination de l'équipe (corrélation +0,72 à +0,88). Offensif : 2 à 14 %.
2. **L'ajustement à l'adversaire ne déplace presque personne, même en Serie A**, seul calendrier déséquilibré (deux poules de cinq après 18 journées) : écart médian avec le par 90 de 3 à 6 %, au plus 2 joueuses qui bougent de 20 points.
3. **Entrer en jeu, à fenêtre égale** : on compare chaque joueuse à elle-même, entre ses entrées à partir de la 65e minute et ses matchs complets **sur la même fenêtre** (65e → fin). 200 joueuses des quatre ligues, au moins 3 matchs de chaque : pressions ×1,33 [IC 95 % 1,25-1,42], actions progressives ×1,25 [1,10-1,40], ballons gagnés ×1,09 [1,01-1,18], xG hors penalties ×1,48 [1,13-1,92], xA ×1,48 [1,05-2,09]. L'effet sur les pressions se retrouve dans chaque ligue (×1,22 à ×1,38) ; celui sur l'xG varie selon la ligue (nul en Frauen-Bundesliga et en Serie A). La part de possession de l'équipe ne change pas entre entrée et titularisation : ce n'est pas un effet de domination. Le par 90 d'une remplaçante surestime donc ce qu'elle ferait sur un match entier, surtout pour le pressing.
4. **Hiérarchie des ligues** : passer du par 90 au par possession change peu l'ordre des ligues (xG : la WSL passe de 1re à 3e, la Serie A de 3e à 1re, sur des écarts faibles). Les percentiles « quatre ligues » ne corrigent pas le niveau de chaque championnat.

## Application

`streamlit_app.py` (thème dans `.streamlit/config.toml`, charte : fond crème, vert d'eau, DM Serif Display et Lato).
- **Classements** : choisir le championnat (ou les quatre), le poste, l'indicateur, deux versions et le seuil ; nuage « percentile avant / après », joueuses qui gagnent et perdent le plus de places, classement complet.
- **Fiche joueuse** : percentiles des cinq indicateurs dans les deux versions.
- **Entrer en jeu** : le test « même fenêtre », par championnat.
- **Méthode et limites**.

Déploiement sur Streamlit Community Cloud : fichier principal `streamlit_app.py`, dépendances dans `requirements.txt`. L'application ne lit que `data/processed/player_season_versions_all_2324.csv` et `outputs/comparaison/tables/` (versionnés) : aucun téléchargement nécessaire.

## Tests

```bash
python -m pytest tests
```

12 tests sur données synthétiques (aucun téléchargement) : conversions d'horloge, temps de jeu à partir des événements (remplacement, expulsion), possession pendant la présence, événements administratifs exclus, actions progressives, règles des indicateurs (penalty exclu, xA, coups de pied arrêtés, récupérations ratées), facteur adversaire sans l'équipe de la joueuse, percentiles au sein du poste, corrélation de rang, choix des ligues, découpage en phases, lancement de l'application.

## Limites
- Données d'événements, pas de tracking : les opportunités sans ballon (appels, courses) et l'intensité physique ne sont pas mesurées.
- Une saison par ligue : petits échantillons pour les joueuses peu utilisées.
- Les ajustements sont des modèles : ils réduisent un biais, ils ne mesurent pas une « vraie » valeur.
- L'effet « entrer en jeu » est mesuré, pas expliqué (fraîcheur, consignes, état du score).

Data: StatsBomb.
