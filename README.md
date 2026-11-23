# womens-football-opportunity

Mesurer la performance des joueuses **selon les opportunités qu'elles ont eues** (temps de jeu, possession de l'équipe et de l'adversaire, ballons reçus, niveau de l'adversaire), en football féminin, sur StatsBomb Open Data.

Idée inspirée de Bozděch (2026, *PLOS ONE*, doi 10.1371/journal.pone.0359538) : mesurer la performance selon les opportunités de l'exprimer. Normalisation par la possession et percentiles par poste inspirés des analyses SkillCorner de Victoria Friss de Kereki.

## Étape 1 — Données et table « joueuse × match » (FA WSL 2023/24)

```bash
pip install -r requirements.txt
python src/download.py data_raw              # 132 matchs : événements + compositions (~410 Mo, non versionnés)
python src/build_player_match.py data_raw data/processed
```

Sortie : `data/processed/player_match_wsl_2324.csv` (3 984 lignes, 132 matchs, 296 joueuses, 12 équipes × 22 matchs).

### Colonnes
| Colonne | Définition |
|---|---|
| `match_id`, `match_date`, `match_week` | Match |
| `team`, `opponent`, `home`, `team_goals`, `opp_goals` | Équipe, adversaire, domicile, score final |
| `player_id`, `player` | Joueuse (surnom StatsBomb si disponible) |
| `starter` | Titulaire |
| `main_position`, `position_group` | Poste le plus fréquent dans ses événements ; groupe GK, CB, FB, DM, CM, AM, W, FW |
| `seconds_played`, `minutes_played` | Temps sur le terrain, temps additionnel compris |
| `match_seconds` | Durée réelle du match (somme des périodes) |
| `team_possessions_on`, `opp_possessions_on` | Possessions commencées pendant sa présence |
| `team_possession_s_on`, `opp_possession_s_on` | Temps de possession « ballon vivant » pendant sa présence (du premier événement de la possession à la fin du dernier) |
| `team_possession_share_on` | Part de possession de l'équipe pendant sa présence |
| `ball_receipts`, `ball_receipts_ok` | Ballons reçus (événements *Ball Receipt*), dont réussis |
| `goals_for_on`, `goals_against_on` | Buts marqués et encaissés par l'équipe pendant sa présence |

### Choix de méthode
- **Temps de jeu reconstruit à partir des événements** (titulaires, remplacements, cartons rouges et seconds jaunes, sorties temporaires *Player Off / Player On*). Les horaires de poste des fichiers de composition sont incohérents dans plusieurs matchs (périodes inversées, joueuses comptées deux fois).
- **Horloge continue** : StatsBomb remet l'horloge à 45:00 en 2e période alors que la 1re peut finir à 47:xx ; tout est converti en temps écoulé réel.
- **Possession « ballon vivant »** : les arrêts de jeu entre deux possessions ne sont attribués à personne (≈ 64 min par match, contre ≈ 101 min de durée totale). Proche de l'esprit des « 30 min de possession » (TIP / OTIP) de SkillCorner, sans être identique (SkillCorner travaille sur du tracking).

### Contrôles
- 11 titulaires pour chacune des 264 feuilles équipe-match.
- Somme des temps joués = 11 × durée du match (à 0,1 % près), sauf deux matchs avec expulsions (Manchester City contre Chelsea, 08/10/2023, deux seconds jaunes ; Aston Villa contre Chelsea, 17/04/2024, rouge à la 3e minute), où le manque correspond au temps joué en infériorité.
- Pour les joueuses ayant joué tout le match, buts pour = score final dans 100 % des cas.

## Étape 2 — Indicateurs et leurs quatre versions

```bash
python src/build_indicators.py data_raw data/processed
```

Sorties : `player_match_indicators_wsl_2324.csv` (table de l'étape 1 + comptes) et `player_season_versions_wsl_2324.csv` (304 lignes joueuse-équipe : 8 joueuses ont changé de club en cours de saison ; 152 ont au moins 900 min, 202 au moins 5 matchs de 60 min).

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

Contrôles : 375 npxG pour 402 buts hors penalties et csc ; xA = 69 % du npxG (tous les tirs ne suivent pas une passe) ; ordres de grandeur par poste cohérents (npxG/90 médian : FW 0,32, CB 0,04) ; facteur adversaire centré sur 1.

Premier constat : dans un championnat où chaque équipe affronte toutes les autres deux fois, l'ajustement à l'adversaire ne change presque rien sur une saison (moins de 15 % d'écart avec le par 90, aucune joueuse ne bouge de 20 points de percentile). La normalisation par la possession, elle, change beaucoup les indicateurs défensifs.

## Limites
Données d'événements, pas de tracking : les opportunités sans ballon (appels, courses) ne sont pas mesurées. Une saison par ligue : petits échantillons pour les joueuses peu utilisées.

Data: StatsBomb.
