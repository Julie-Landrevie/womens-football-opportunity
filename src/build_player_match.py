"""Table « joueuse × match » — FA WSL 2023/24 (StatsBomb Open Data).

Une ligne par joueuse ayant joué (temps de jeu > 0) dans un match, avec les
mesures d'opportunité de l'étape 1 :
  - temps de jeu (secondes et minutes, temps additionnel compris), titulaire ou non ;
  - poste principal (le plus de temps joué) et groupe de postes ;
  - possessions de l'équipe et de l'adversaire pendant qu'elle est sur le terrain
    (nombre, et temps « ballon vivant » : du premier événement à la fin du dernier) ;
  - ballons reçus (événements Ball Receipt*, tous et réussis) ;
  - adversaire, domicile/extérieur, score, buts pour/contre pendant sa présence.

Horloge : StatsBomb remet l'horloge à 45:00 au début de la 2e période, alors que
la 1re période peut aller jusqu'à 47:xx. Tout est donc converti en « temps écoulé »
continu (somme des durées réelles des périodes précédentes + temps dans la période).

Usage : python src/build_player_match.py [dossier_raw] [dossier_sortie]
Données : StatsBomb Open Data. Crédit : « Data: StatsBomb ».
"""
import json
import sys
from pathlib import Path

import pandas as pd

PERIOD_START_CLOCK = {1: 0, 2: 45 * 60, 3: 90 * 60, 4: 105 * 60}

POSITION_GROUP = {
    "Goalkeeper": "GK",
    "Right Back": "FB", "Left Back": "FB", "Right Wing Back": "FB", "Left Wing Back": "FB",
    "Center Back": "CB", "Right Center Back": "CB", "Left Center Back": "CB",
    "Center Defensive Midfield": "DM", "Right Defensive Midfield": "DM", "Left Defensive Midfield": "DM",
    "Center Midfield": "CM", "Right Center Midfield": "CM", "Left Center Midfield": "CM",
    "Right Midfield": "W", "Left Midfield": "W", "Right Wing": "W", "Left Wing": "W",
    "Center Attacking Midfield": "AM", "Right Attacking Midfield": "AM", "Left Attacking Midfield": "AM",
    "Center Forward": "FW", "Right Center Forward": "FW", "Left Center Forward": "FW",
    "Secondary Striker": "FW",
}


def clock_to_s(txt: str) -> float:
    m, s = txt.split(":")
    return int(m) * 60 + float(s)


def ts_to_s(ts: str) -> float:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def overlap(a0, a1, b0, b1) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def process_match(match: dict, events: list, lineups: list) -> list[dict]:
    mid = match["match_id"]
    home_id = match["home_team"]["home_team_id"]
    away_id = match["away_team"]["away_team_id"]

    # Durées réelles des périodes (événements Half End) → décalages en temps écoulé.
    dur = {}
    for e in events:
        if e["type"]["name"] == "Half End":
            dur[e["period"]] = max(dur.get(e["period"], 0), ts_to_s(e["timestamp"]))
    periods = sorted(p for p in dur if p <= 4)  # 5 = tirs au but, exclus
    offset, acc = {}, 0.0
    for p in periods:
        offset[p] = acc
        acc += dur[p]
    match_end = acc

    def ev_t(e):  # temps écoulé d'un événement
        return offset[e["period"]] + ts_to_s(e["timestamp"])

    def lu_t(clock: str | None, period: int | None) -> float:
        if clock is None or period is None:
            return match_end
        if period not in offset:  # prolongations absentes, etc.
            return match_end
        within = clock_to_s(clock) - PERIOD_START_CLOCK[period]
        return min(offset[period] + max(within, 0.0), offset[period] + dur[period])

    ev = [e for e in events if e["period"] in offset]

    # Possessions : équipe, début, fin « ballon vivant », fin « jusqu'à la suivante ».
    poss = {}
    for e in ev:
        t0 = ev_t(e)
        t1 = t0 + float(e.get("duration") or 0.0)
        k = e["possession"]
        p = poss.setdefault(k, {"team": e["possession_team"]["id"], "start": t0,
                                "end": t1, "period": e["period"]})
        p["start"] = min(p["start"], t0)
        p["end"] = max(p["end"], t1)
    poss_df = pd.DataFrame.from_dict(poss, orient="index").sort_index()
    # borne : une possession « vivante » ne dépasse pas la fin de sa période
    poss_df["end"] = [min(r.end, offset[r.period] + dur[r.period]) for r in poss_df.itertuples()]

    # Événements par joueuse
    receipts, receipts_ok, goals = {}, {}, []
    for e in ev:
        name = e["type"]["name"]
        if name == "Ball Receipt*" and "player" in e:
            pid = e["player"]["id"]
            receipts[pid] = receipts.get(pid, 0) + 1
            if "outcome" not in e.get("ball_receipt", {}):
                receipts_ok[pid] = receipts_ok.get(pid, 0) + 1
        if name == "Shot" and e["shot"]["outcome"]["name"] == "Goal":
            goals.append((ev_t(e), e["team"]["id"]))
        if name == "Own Goal For":
            goals.append((ev_t(e), e["team"]["id"]))

    # Temps de présence reconstruit à partir des événements (les horaires des
    # compositions sont incohérents dans certains matchs) :
    # titulaires ouverts à 0 ; Substitution = sortie + entrée ; carton rouge ou
    # second jaune = sortie ; Player Off / Player On = sortie et retour temporaires.
    open_at, spells_by = {}, {}

    def close(pid, t):
        if pid in open_at:
            t0 = open_at.pop(pid)
            if t > t0:
                spells_by.setdefault(pid, []).append((t0, t))

    for e in ev:
        n, t = e["type"]["name"], ev_t(e)
        if n == "Starting XI":
            for x in e["tactics"]["lineup"]:
                open_at[x["player"]["id"]] = 0.0
        elif n == "Substitution":
            close(e["player"]["id"], t)
            open_at[e["substitution"]["replacement"]["id"]] = t
        elif n in ("Bad Behaviour", "Foul Committed") and "player" in e:
            card = (e.get("bad_behaviour") or e.get("foul_committed") or {}).get("card")
            if card and card["name"] in ("Red Card", "Second Yellow"):
                close(e["player"]["id"], t)
        elif n == "Player Off" and "player" in e:
            close(e["player"]["id"], t)
        elif n == "Player On" and "player" in e:
            open_at.setdefault(e["player"]["id"], t)
    for pid in list(open_at):
        close(pid, match_end)

    # Poste principal : poste le plus fréquent dans les événements de la joueuse.
    pos_count = {}
    for e in ev:
        if "player" in e and "position" in e:
            d = pos_count.setdefault(e["player"]["id"], {})
            d[e["position"]["name"]] = d.get(e["position"]["name"], 0) + 1

    rows = []
    for team in lineups:
        tid = team["team_id"]
        opp_id = away_id if tid == home_id else home_id
        opp_name = (match["away_team"]["away_team_name"] if tid == home_id
                    else match["home_team"]["home_team_name"])
        gf = match["home_score"] if tid == home_id else match["away_score"]
        ga = match["away_score"] if tid == home_id else match["home_score"]
        for pl in team["lineup"]:
            spells = [(a, b, None) for a, b in spells_by.get(pl["player_id"], [])]
            if not spells:
                continue
            secs = sum(b - a for a, b, _ in spells)
            by_pos = pos_count.get(pl["player_id"]) or {
                (pl["positions"][0]["position"] if pl["positions"] else "?"): 1}
            main_pos = max(by_pos, key=by_pos.get)

            n_tp = n_op = t_tp = t_op = 0.0
            for r in poss_df.itertuples():
                ov = sum(overlap(r.start, r.end, a, b) for a, b, _ in spells)
                started_in = any(a <= r.start < b for a, b, _ in spells)
                if r.team == tid:
                    t_tp += ov
                    n_tp += started_in
                else:
                    t_op += ov
                    n_op += started_in
            g_for = sum(1 for t, team_id in goals if team_id == tid and any(a <= t <= b for a, b, _ in spells))
            g_ag = sum(1 for t, team_id in goals if team_id != tid and any(a <= t <= b for a, b, _ in spells))

            rows.append({
                "match_id": mid,
                "match_date": match["match_date"],
                "match_week": match.get("match_week"),
                "team_id": tid,
                "team": team["team_name"],
                "opponent_id": opp_id,
                "opponent": opp_name,
                "home": tid == home_id,
                "team_goals": gf,
                "opp_goals": ga,
                "player_id": pl["player_id"],
                "player": pl["player_nickname"] or pl["player_name"],
                "starter": any(a == 0.0 for a, _, _ in spells),
                "main_position": main_pos,
                "position_group": POSITION_GROUP.get(main_pos, "?"),
                "n_positions": len(by_pos),
                "seconds_played": round(secs, 1),
                "minutes_played": round(secs / 60, 2),
                "match_seconds": round(match_end, 1),
                "team_possessions_on": int(n_tp),
                "opp_possessions_on": int(n_op),
                "team_possession_s_on": round(t_tp, 1),
                "opp_possession_s_on": round(t_op, 1),
                "ball_receipts": receipts.get(pl["player_id"], 0),
                "ball_receipts_ok": receipts_ok.get(pl["player_id"], 0),
                "goals_for_on": g_for,
                "goals_against_on": g_ag,
            })
    return rows


def main(raw_dir: str = "data_raw", out_dir: str = "data/processed") -> None:
    raw, out = Path(raw_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    matches = json.loads(next(raw.glob("matches_*.json")).read_text())
    rows = []
    for m in matches:
        mid = m["match_id"]
        ev = json.loads((raw / "events" / f"{mid}.json").read_text())
        lu = json.loads((raw / "lineups" / f"{mid}.json").read_text())
        rows += process_match(m, ev, lu)
    df = pd.DataFrame(rows).sort_values(["match_date", "match_id", "team", "starter", "player"],
                                        ascending=[True, True, True, False, True])
    df["team_possession_share_on"] = (df.team_possession_s_on /
                                      (df.team_possession_s_on + df.opp_possession_s_on)).round(3)
    df.to_csv(out / "player_match_wsl_2324.csv", index=False)
    print(f"{len(df)} lignes joueuse × match, {df.match_id.nunique()} matchs, "
          f"{df.player_id.nunique()} joueuses → {out/'player_match_wsl_2324.csv'}")


if __name__ == "__main__":
    main(*sys.argv[1:])
