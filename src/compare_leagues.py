"""Étape 4 — Comparaison des quatre championnats féminins 2023/24.

Entrées : tables des étapes 2 et 3 de chaque ligue (data/processed/, outputs/<slug>/tables/)
          et événements bruts (data_raw/<slug>/events) pour le test « même fenêtre ».
Sorties :
  - data/processed/player_season_versions_all_2324.csv : les quatre ligues réunies (utilisée par
    l'application, qui calcule les percentiles selon la sélection) ;
  - outputs/comparaison/tables/*.csv et outputs/comparaison/resultats_etape4.md.

Questions :
  1. Contexte : possession, écarts de domination, buts et xG par ligue.
  2. L'effet de la normalisation par possession est-il le même dans chaque ligue ?
  3. L'ajustement à l'adversaire sert-il en Serie A, seul calendrier déséquilibré (poules) ?
  4. L'effet « entrée en jeu » se retrouve-t-il partout ? Test « même fenêtre » : remplaçantes
     entrées à partir de la 65e minute contre les mêmes joueuses titulaires sur la même fenêtre
     (65e → fin), quatre ligues réunies.
  5. Environnement : la hiérarchie des ligues change-t-elle entre par 90 et par possession ?

Usage : python src/compare_leagues.py [dossier_processed] [dossier_outputs] [dossier_raw]
Données : StatsBomb Open Data. Crédit : « Data: StatsBomb ».
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_rankings import LABELS, N_BOOT, pct_in_position
from build_indicators import INDICATORS, match_counts
from leagues import LEAGUES

LATE_MINUTE = 65
RNG = np.random.default_rng(42)
VERSIONS = ["total", "p90", "poss", "adj"]


def load_all(proc: Path, name: str) -> pd.DataFrame:
    return pd.concat([pd.read_csv(proc / f"{name}_{lg['slug']}.csv") for lg in LEAGUES.values()],
                     ignore_index=True)


def load_tables(out_root: Path, name: str) -> pd.DataFrame:
    return pd.concat([pd.read_csv(out_root / lg["slug"] / "tables" / f"{name}.csv")
                      for lg in LEAGUES.values()], ignore_index=True)


# ------------------------------------------------------------ table commune pour l'application
def combined_versions(proc: Path) -> pd.DataFrame:
    sv = load_all(proc, "player_season_versions")
    sv.insert(1, "league_name", sv.league.map({k: v["name"] for k, v in LEAGUES.items()}))
    return sv  # les percentiles sont calculés dans l'application, selon la sélection


# ---------------------------------------------------------------------------- 1. contexte
def context(proc: Path) -> pd.DataFrame:
    pm = load_all(proc, "player_match_indicators")
    rows = []
    for key, g in pm.groupby("league", sort=False):
        full = g[g.seconds_played >= g.match_seconds - 1]
        share = full.groupby("team").team_possession_share_on.mean()
        tm = g.groupby(["match_id", "team_id"]).agg(goals=("team_goals", "first"))
        n_matches = g.match_id.nunique()
        rows.append({"league": key, "ligue": LEAGUES[key]["name"], "equipes": g.team_id.nunique(),
                     "matchs": n_matches, "joueuses": g.player_id.nunique(),
                     "duree_match_min": round(g.groupby("match_id").match_seconds.first().mean() / 60, 1),
                     "possession_par_match_min": round(((full.team_possession_s_on + full.opp_possession_s_on) / 60).mean(), 1),
                     "possession_equipe_min": round(share.min(), 3), "possession_equipe_max": round(share.max(), 3),
                     "ecart_type_possession": round(share.std(), 3),
                     "buts_par_match": round(tm.goals.sum() / n_matches, 2),
                     "npxg_par_match": round(g.npxg.sum() / n_matches, 2),
                     "pressions_par_match": round(g.pressures.sum() / n_matches, 1),
                     "entrees_par_match": round((~g.starter).sum() / n_matches, 1)})
    return pd.DataFrame(rows)


# ----------------------------------------------------- 4. test « même fenêtre » (65e → fin)
def same_window(proc: Path, raw_root: Path) -> pd.DataFrame:
    """Par joueuse : comptes et secondes en entrée tardive, et sur la fenêtre 65e → fin
    quand elle est titulaire et joue tout le match."""
    rows = []
    for key, lg in LEAGUES.items():
        pm = pd.read_csv(proc / f"player_match_indicators_{lg['slug']}.csv")
        pm = pm[pm.position_group != "GK"]
        for mid, g in pm.groupby("match_id"):
            ev = json.loads((raw_root / lg["slug"] / "events" / f"{mid}.json").read_text())
            dur = {}
            for e in ev:
                if e["type"]["name"] == "Half End" and e["period"] <= 2:
                    h, m, s = e["timestamp"].split(":")
                    dur[e["period"]] = max(dur.get(e["period"], 0), int(h) * 3600 + int(m) * 60 + float(s))
            cut = dur[1] + (LATE_MINUTE - 45) * 60                 # 65e minute en temps écoulé
            late_secs = dur[1] + dur[2] - cut
            late_counts = match_counts([e for e in ev if e["period"] == 2 and e["minute"] >= LATE_MINUTE])
            for r in g.itertuples():
                entry = r.match_seconds - r.seconds_played          # entrée (si elle finit le match)
                if r.starter and r.seconds_played >= r.match_seconds - 1:
                    c = late_counts.get(r.player_id, dict.fromkeys(INDICATORS, 0.0))
                    rows.append({"league": key, "player_id": r.player_id, "groupe": "titulaire_fenetre",
                                 "secondes": late_secs, **{k: c[k] for k in INDICATORS}})
                elif (not r.starter) and entry >= cut - 1 and abs(r.match_seconds - (entry + r.seconds_played)) < 1:
                    rows.append({"league": key, "player_id": r.player_id, "groupe": "entree_tardive",
                                 "secondes": r.seconds_played, **{k: getattr(r, k) for k in INDICATORS}})
    return pd.DataFrame(rows)


def same_window_ratios(sw: pd.DataFrame, min_each: int = 3) -> pd.DataFrame:
    sw = sw.assign(pkey=sw.league + "_" + sw.player_id.astype(str))
    n = sw.groupby(["pkey", "groupe"]).size().unstack(fill_value=0)
    keep = n[(n.get("titulaire_fenetre", 0) >= min_each) & (n.get("entree_tardive", 0) >= min_each)].index
    sw = sw[sw.pkey.isin(keep)]
    agg = sw.groupby(["league", "pkey", "groupe"])[INDICATORS + ["secondes"]].sum().reset_index()

    def ratio(a: pd.DataFrame, k: str) -> float:
        s, t = a[a.groupe == "entree_tardive"], a[a.groupe == "titulaire_fenetre"]
        return (s[k].sum() / s.secondes.sum()) / (t[k].sum() / t.secondes.sum())

    rows = []
    scopes = {"4 ligues": agg, **{LEAGUES[k]["name"]: g for k, g in agg.groupby("league")}}
    for scope, a in scopes.items():
        players = a.pkey.unique()
        by_p = {p: g for p, g in a.groupby("pkey")}
        for k in INDICATORS:
            boots = []
            for _ in range(N_BOOT):
                boots.append(ratio(pd.concat([by_p[p] for p in RNG.choice(players, len(players))]), k))
            lo, hi = np.nanpercentile(boots, [2.5, 97.5])
            s, t = a[a.groupe == "entree_tardive"], a[a.groupe == "titulaire_fenetre"]
            rows.append({"perimetre": scope, "joueuses": len(players), "indicateur": k,
                         "p90_titulaire_fenetre": round(t[k].sum() / t.secondes.sum() * 5400, 3),
                         "p90_entree_tardive": round(s[k].sum() / s.secondes.sum() * 5400, 3),
                         "minutes_titulaire_fenetre": round(t.secondes.sum() / 60),
                         "minutes_entree_tardive": round(s.secondes.sum() / 60),
                         "ratio": round(ratio(a, k), 2), "ic95_bas": round(lo, 2), "ic95_haut": round(hi, 2)})
    return pd.DataFrame(rows)


# ------------------------------------------------------- 5. hiérarchie des ligues (environnement)
def league_levels(sv: pd.DataFrame) -> pd.DataFrame:
    e = sv[sv.eligible_5x60 & (sv.position_group != "GK")]
    rows = []
    for k in INDICATORS:
        for v in ["p90", "poss"]:
            med = e.groupby("league")[f"{k}_{v}"].median()
            for key, val in med.items():
                rows.append({"indicateur": k, "version": v, "league": key, "mediane": round(val, 3),
                             "rang": int(med.rank(ascending=False)[key])})
    return pd.DataFrame(rows)


def pooled_moves(sv: pd.DataFrame) -> pd.DataFrame:
    """Toutes ligues confondues : déplacement p90 → poss et part due à la ligue."""
    e = sv[sv.eligible_5x60 & (sv.position_group != "GK")].copy()
    rows = []
    for k in INDICATORS:
        d = pct_in_position(e, f"{k}_poss") - pct_in_position(e, f"{k}_p90")
        moved = d.abs() >= 0.2
        rows.append({"indicateur": k, "n": len(e), "bougent_20pts": int(moved.sum()),
                     "part_bougent": round(moved.mean(), 3),
                     "corr_delta_possession": round(d.corr(e.team_poss_share), 2),
                     **{f"delta_moyen_{lg}": round(d[e.league == lg].mean() * 100, 1) for lg in LEAGUES}})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- résumé
def fmt_ci(r) -> str:
    return f"{r.ratio:.2f} [{r.ic95_bas:.2f}-{r.ic95_haut:.2f}]"


def summary(ctx, moves, pooled, adj_season, adj_half, subs, late, sw, levels, stab) -> str:
    names = {k: v["name"] for k, v in LEAGUES.items()}
    keys = list(LEAGUES)
    L = ["# Étape 4 — Comparaison des quatre championnats féminins 2023/24", "",
         "Généré par `src/compare_leagues.py`. Joueuses de champ avec au moins 5 matchs de 60 min ; "
         "percentiles au sein du groupe de postes. Data: StatsBomb.", "",
         "## 1. Contexte", "",
         "| Ligue | Équipes | Matchs | Joueuses | Possession / match | Possession des équipes | Buts / match | xG hors pen. / match | Entrées en jeu / match |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in ctx.itertuples():
        L.append(f"| {r.ligue} | {r.equipes} | {r.matchs} | {r.joueuses} | {r.possession_par_match_min} min | "
                 f"{r.possession_equipe_min:.0%} à {r.possession_equipe_max:.0%} | {r.buts_par_match} | "
                 f"{r.npxg_par_match} | {r.entrees_par_match} |")
    L += ["", "## 2. Du par 90 au par possession : part des joueuses qui bougent d'au moins 20 points", "",
          "| Indicateur | " + " | ".join(names[k] for k in keys) + " | 4 ligues réunies |",
          "|---|" + "---|" * (len(keys) + 1)]
    pm_ = pooled.set_index("indicateur")
    for k in INDICATORS:
        cells = []
        for lg in keys:
            r = moves[(moves.league == lg) & (moves.indicateur == k)].iloc[0]
            cells.append(f"{r.part_bougent:.0%} ({r.corr_delta_possession:+.2f})")
        L.append(f"| {LABELS[k]} | " + " | ".join(cells) +
                 f" | {pm_.loc[k, 'part_bougent']:.0%} ({pm_.loc[k, 'corr_delta_possession']:+.2f}) |")
    L += ["", "Entre parenthèses : corrélation entre le déplacement et la part de possession de l'équipe.", "",
          "## 3. Ajustement à l'adversaire", "",
          "Saison complète, par 90 → ajusté : joueuses qui bougent d'au moins 20 points.", "",
          "| Indicateur | " + " | ".join(names[k] for k in keys) + " |", "|---|" + "---|" * len(keys)]
    for k in INDICATORS:
        L.append(f"| {LABELS[k]} | " + " | ".join(
            str(int(adj_season[(adj_season.league == lg) & (adj_season.indicateur == k)].bougent_20pts.iloc[0]))
            for lg in keys) + " |")
    L += ["", "Par phase (joueuses ≥ 450 min) : écart médian entre ajusté et par 90, et joueuses qui bougent de 20 points.", "",
          "| Ligue | Phase | Adversaires distincts (min.) | xG hors pen. | Actions progressives | Pressions |", "|---|---|---|---|---|---|"]
    for (lg, ph), g in adj_half[adj_half.groupe.str.startswith("≥ 450")].groupby(["league", "moitie"], sort=False):
        gi = g.set_index("indicateur")
        L.append(f"| {names[lg]} | {ph} | {gi.adversaires_distincts_par_equipe.iloc[0]} | " + " | ".join(
            f"{gi.loc[k, 'ecart_adj_p90_median']:.1%} ({int(gi.loc[k, 'bougent_20pts'])})"
            for k in ["npxg", "prog", "pressures"]) + " |")
    L += ["", "## 4. Entrer en jeu plutôt que commencer", "",
          "Mêmes joueuses (au moins 3 matchs de chaque), ratio global par 90 entrée / titulaire [IC 95 %] :", "",
          "| Indicateur | " + " | ".join(names[k] for k in keys) + " |", "|---|" + "---|" * len(keys)]
    for k in INDICATORS + ["ball_receipts", "part_possession_equipe"]:
        cells = []
        for lg in keys:
            r = subs[(subs.league == lg) & (subs.indicateur == k)].iloc[0]
            cells.append(f"{r.ratio_entree_sur_titulaire:.2f} [{r.ic95_bas:.2f}-{r.ic95_haut:.2f}]")
        lab = LABELS.get(k, {"ball_receipts": "ballons reçus", "part_possession_equipe": "part de possession"}.get(k, k))
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    L += ["", "Titulaires qui jouent tout le match : ratio par 90 après / avant la 65e minute.", "",
          "| Indicateur | " + " | ".join(names[k] for k in keys) + " |", "|---|" + "---|" * len(keys)]
    for k in INDICATORS:
        L.append(f"| {LABELS[k]} | " + " | ".join(
            f"{late[(late.league == lg) & (late.indicateur == k)].ratio_fin_sur_avant.iloc[0]:.2f}" for lg in keys) + " |")
    L += ["", f"**Test « même fenêtre »** : remplaçantes entrées à partir de la {LATE_MINUTE}e minute contre les mêmes "
          f"joueuses titulaires, sur la même fenêtre ({LATE_MINUTE}e → fin du match). Au moins 3 matchs de chaque.", "",
          "| Périmètre | Joueuses | Indicateur | Titulaire (fenêtre) | Entrée tardive | Ratio [IC 95 %] |",
          "|---|---|---|---|---|---|"]
    for r in sw.itertuples():
        L.append(f"| {r.perimetre} | {r.joueuses} | {LABELS[r.indicateur]} | {r.p90_titulaire_fenetre} | "
                 f"{r.p90_entree_tardive} | {fmt_ci(r)} |")
    L += ["", "## 5. Hiérarchie des ligues : médiane par 90 et par possession (rang entre parenthèses)", "",
          "| Indicateur | Version | " + " | ".join(names[k] for k in keys) + " |", "|---|---|" + "---|" * len(keys)]
    for (k, v), g in levels.groupby(["indicateur", "version"], sort=False):
        gi = g.set_index("league")
        L.append(f"| {LABELS[k]} | {LABELS[v]} | " + " | ".join(
            f"{gi.loc[lg, 'mediane']} ({gi.loc[lg, 'rang']})" for lg in keys) + " |")
    L += ["", "## 6. Stabilité au sein du poste (1re phase contre reste de la saison)", "",
          "| Indicateur | Version | " + " | ".join(names[k] for k in keys) + " |", "|---|---|" + "---|" * len(keys)]
    for k in INDICATORS:
        for v in ["p90", "poss"]:
            L.append(f"| {LABELS[k]} | {LABELS[v]} | " + " | ".join(
                f"{stab[(stab.league == lg) & (stab.indicateur == k) & (stab.version == v)].spearman_dans_poste.iloc[0]:.2f}"
                for lg in keys) + " |")
    return "\n".join(L) + "\n"


def main(proc_dir: str = "data/processed", out_root: str = "outputs", raw_root: str = "data_raw") -> None:
    proc, out_root, raw_root = Path(proc_dir), Path(out_root), Path(raw_root)
    out = out_root / "comparaison"
    (out / "tables").mkdir(parents=True, exist_ok=True)

    sv = combined_versions(proc)
    sv.to_csv(proc / "player_season_versions_all_2324.csv", index=False)

    ctx = context(proc)
    rc = load_tables(out_root, "changements_classement")
    moves = rc[(rc.seuil == "5 matchs de 60 min") & (rc.de == "p90") & (rc.vers == "poss")]
    adj_season = rc[(rc.seuil == "5 matchs de 60 min") & (rc.de == "p90") & (rc.vers == "adj")]
    adj_half = load_tables(out_root, "ajustement_demi_saison")
    subs = load_tables(out_root, "titulaire_contre_entree")
    late = load_tables(out_root, "controle_fin_de_match")
    stab = load_tables(out_root, "stabilite")
    stab = stab[stab.decoupage == "1re phase / reste"]
    sw = same_window_ratios(same_window(proc, raw_root))
    levels = league_levels(sv)
    pooled = pooled_moves(sv)

    tables = {"contexte": ctx, "possession_par_ligue": moves, "deplacements_4_ligues": pooled,
              "meme_fenetre": sw, "hierarchie_ligues": levels}
    for name, df in tables.items():
        df.to_csv(out / "tables" / f"{name}.csv", index=False)
    (out / "resultats_etape4.md").write_text(
        summary(ctx, moves, pooled, adj_season, adj_half, subs, late, sw, levels, stab), encoding="utf-8")
    print(f"Comparaison : {len(tables)} tables dans {out / 'tables'}, résumé {out / 'resultats_etape4.md'}, "
          f"table commune {proc / 'player_season_versions_all_2324.csv'} ({len(sv)} lignes)")


if __name__ == "__main__":
    main(*sys.argv[1:])
