"""Étape 2 — Indicateurs de performance et leurs quatre versions, par ligue.

Entrées : data_raw/<slug>/events/*.json, data/processed/player_match_<slug>.csv (étape 1).
Sorties :
  - data/processed/player_match_indicators_<slug>.csv : table joueuse × match + comptes ;
  - data/processed/player_season_versions_<slug>.csv : une ligne par joueuse (et équipe),
    chaque indicateur en 4 versions : total, par 90, par possession, ajusté à l'adversaire.

Indicateurs (5) :
  offensifs  npxg       xG hors penalties (StatsBomb)
             xa         xG des tirs qui suivent une passe de la joueuse (passe clé)
             prog       passes réussies et conduites progressives, jeu courant
  défensifs  pressures  pressions
             ball_wins  tacles gagnés + interceptions gagnées + récupérations réussies

Versions :
  total      somme sur la saison
  p90        total / minutes × 90
  poss       offensifs : par 30 min de possession de l'équipe pendant sa présence ;
             défensifs : par 30 min de possession adverse pendant sa présence
             (logique TIP / OTIP de SkillCorner ; ici, temps de possession
             reconstruit à partir des événements de jeu)
  adj        par 90, ajusté au niveau de l'adversaire : total ÷ Σ(minutes/90 × facteur
             de l'adversaire). Facteur = ce que les équipes produisent contre cet
             adversaire (par 90, toutes joueuses) ÷ moyenne de la ligue, calculé en
             excluant l'équipe de la joueuse (sinon elle se compare à elle-même).

Usage : python src/build_indicators.py <wsl|fbl|ligaf|seriea|all> [dossier_raw] [dossier_processed]
Données : StatsBomb Open Data. Crédit : « Data: StatsBomb ».
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

from leagues import LEAGUES, resolve

GOAL = (120.0, 40.0)
SET_PIECES = {"Corner", "Free Kick", "Goal Kick", "Kick Off", "Throw-in"}
WON = {"Won", "Success In Play", "Success Out"}
OFFENSIVE = ["npxg", "xa", "prog"]
DEFENSIVE = ["pressures", "ball_wins"]
INDICATORS = OFFENSIVE + DEFENSIVE
PROG_MIN_X = 48.0     # départ au-delà des 40 % de son propre camp
PROG_RATIO = 0.75     # arrivée au moins 25 % plus près du but


def dist_goal(loc) -> float:
    return math.hypot(GOAL[0] - loc[0], GOAL[1] - loc[1])


def is_progressive(start, end) -> bool:
    return start[0] >= PROG_MIN_X and dist_goal(end) <= PROG_RATIO * dist_goal(start)


def match_counts(events: list) -> dict:
    """Comptes par (match, joueuse) pour un match."""
    out = {}

    def add(pid, key, val=1.0):
        d = out.setdefault(pid, dict.fromkeys(INDICATORS, 0.0))
        d[key] += val

    shot_xg = {e["id"]: e["shot"].get("statsbomb_xg", 0.0) for e in events
               if e["type"]["name"] == "Shot" and e["shot"]["type"]["name"] != "Penalty"}
    for e in events:
        if "player" not in e or e.get("period", 0) > 4:
            continue
        pid, t = e["player"]["id"], e["type"]["name"]
        if t == "Shot" and e["id"] in shot_xg:
            add(pid, "npxg", shot_xg[e["id"]])
        elif t == "Pass":
            p = e["pass"]
            if p.get("assisted_shot_id") in shot_xg:
                add(pid, "xa", shot_xg[p["assisted_shot_id"]])
            if ("outcome" not in p and p.get("type", {}).get("name") not in SET_PIECES
                    and is_progressive(e["location"], p["end_location"])):
                add(pid, "prog")
        elif t == "Carry":
            if is_progressive(e["location"], e["carry"]["end_location"]):
                add(pid, "prog")
        elif t == "Pressure":
            add(pid, "pressures")
        elif t == "Duel":
            d = e["duel"]
            if d.get("type", {}).get("name") == "Tackle" and d.get("outcome", {}).get("name") in WON:
                add(pid, "ball_wins")
        elif t == "Interception":
            if e["interception"]["outcome"]["name"] in WON:
                add(pid, "ball_wins")
        elif t == "Ball Recovery":
            if not (e.get("ball_recovery") or {}).get("recovery_failure"):
                add(pid, "ball_wins")
    return out


def opponent_factors(pm: pd.DataFrame) -> pd.DataFrame:
    """Facteur adversaire par (équipe de la joueuse, adversaire, indicateur), sans l'équipe."""
    tm = (pm.groupby(["match_id", "team_id", "opponent_id"])
            .agg(**{k: (k, "sum") for k in INDICATORS},
                 team_min=("minutes_played", "sum"))
            .reset_index())
    tm["team_min"] /= 11  # minutes « d'équipe »
    league = {k: tm[k].sum() / tm.team_min.sum() for k in INDICATORS}
    rows = []
    for team in tm.team_id.unique():
        others = tm[tm.team_id != team]
        by_opp = others.groupby("opponent_id")
        for opp, g in by_opp:
            if opp == team:
                continue
            r = {"team_id": team, "opponent_id": opp}
            for k in INDICATORS:
                r[f"f_{k}"] = (g[k].sum() / g.team_min.sum()) / league[k]
            rows.append(r)
    return pd.DataFrame(rows)


def season_versions(pm: pd.DataFrame) -> pd.DataFrame:
    fac = opponent_factors(pm)
    pm = pm.merge(fac, on=["team_id", "opponent_id"], how="left")
    for k in INDICATORS:
        pm[f"exp90_{k}"] = pm.minutes_played / 90 * pm[f"f_{k}"]
    agg = {k: (k, "sum") for k in INDICATORS}
    agg.update({f"exp90_{k}": (f"exp90_{k}", "sum") for k in INDICATORS})
    agg.update(
        player=("player", "first"),
        position_group=("position_group", lambda s: s.mode().iat[0]),
        matches=("match_id", "nunique"),
        starts=("starter", "sum"),
        matches_60=("minutes_played", lambda s: int((s >= 60).sum())),
        minutes=("minutes_played", "sum"),
        team_poss_min=("team_possession_s_on", lambda s: s.sum() / 60),
        opp_poss_min=("opp_possession_s_on", lambda s: s.sum() / 60),
        team_poss_share=("team_possession_share_on", "mean"),
    )
    s = pm.groupby(["player_id", "team"]).agg(**agg).reset_index()
    out = s[["player_id", "player", "team", "position_group", "matches", "starts",
             "matches_60", "minutes", "team_poss_min", "opp_poss_min", "team_poss_share"]].copy()
    for k in INDICATORS:
        poss = s.team_poss_min if k in OFFENSIVE else s.opp_poss_min
        out[f"{k}_total"] = s[k]
        out[f"{k}_p90"] = s[k] / s.minutes * 90
        out[f"{k}_poss"] = s[k] / poss * 30
        out[f"{k}_adj"] = s[k] / s[f"exp90_{k}"]
    out["eligible_900"] = out.minutes >= 900
    out["eligible_5x60"] = out.matches_60 >= 5
    return out.round(4)


def build_league(key: str, raw_root: str = "data_raw", proc_dir: str = "data/processed") -> pd.DataFrame:
    lg = LEAGUES[key]
    raw, proc = Path(raw_root) / lg["slug"], Path(proc_dir)
    pm = pd.read_csv(proc / f"player_match_{lg['slug']}.csv")
    rows = []
    for mid in pm.match_id.unique():
        ev = json.loads((raw / "events" / f"{mid}.json").read_text())
        for pid, d in match_counts(ev).items():
            rows.append({"match_id": mid, "player_id": pid, **d})
    counts = pd.DataFrame(rows)
    pm = pm.merge(counts, on=["match_id", "player_id"], how="left")
    pm[INDICATORS] = pm[INDICATORS].fillna(0.0)
    pm.to_csv(proc / f"player_match_indicators_{lg['slug']}.csv", index=False)
    sv = season_versions(pm)
    sv.insert(0, "league", key)
    sv.to_csv(proc / f"player_season_versions_{lg['slug']}.csv", index=False)
    print(f"{lg['name']} : {len(pm)} lignes joueuse × match ; {len(sv)} joueuses-équipes "
          f"({sv.eligible_900.sum()} ≥ 900 min, {sv.eligible_5x60.sum()} ≥ 5 matchs de 60 min)")
    return sv


def main(league: str = "wsl", raw_root: str = "data_raw", proc_dir: str = "data/processed") -> None:
    for key in resolve(league):
        build_league(key, raw_root, proc_dir)


if __name__ == "__main__":
    main(*sys.argv[1:])
