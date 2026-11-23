"""Étape 3 — Classements et stabilité selon la version de l'indicateur (FA WSL 2023/24).

Entrée : data/processed/player_match_indicators_wsl_2324.csv (étape 2).
Sorties dans outputs/tables/ et un résumé chiffré outputs/resultats_etape3.md.

Quatre questions :
  A. Classements : au sein du poste, combien de joueuses changent de place quand on passe
     du total au par 90, du par 90 au par possession, du par 90 à l'ajusté adversaire ?
     Avec les deux seuils de sélection (900 min ; 5 matchs de 60 min ou plus).
  B. Remplaçantes et faible temps de jeu : bruit du par 90 selon le temps de jeu ;
     même joueuse titulaire ou entrée en jeu (comparaison intra-joueuse).
  C. Stabilité : corrélation de rang entre la phase aller (journées 1 à 11) et la phase
     retour (12 à 22), et entre matchs pairs et impairs, pour chaque version.
  D. Ajustement à l'adversaire sur une demi-saison : change-t-il quelque chose ?

Les percentiles sont toujours calculés au sein du groupe de postes, gardiennes exclues.
Usage : python src/analyze_rankings.py [dossier_processed] [dossier_outputs]
Données : StatsBomb Open Data. Crédit : « Data: StatsBomb ».
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from build_indicators import INDICATORS, OFFENSIVE, season_versions

VERSIONS = ["total", "p90", "poss", "adj"]
PAIRS = [("total", "p90"), ("p90", "poss"), ("p90", "adj")]
THRESHOLDS = {"900 min": "eligible_900", "5 matchs de 60 min": "eligible_5x60"}
MOVE = 0.20          # changement de place « notable » : 20 points de percentile
HALF_MIN = 450       # minutes minimales dans chaque moitié pour la stabilité
N_BOOT = 1000
RNG = np.random.default_rng(2324)
LABELS = {"npxg": "xG hors penalties", "xa": "xA", "prog": "actions progressives",
          "pressures": "pressions", "ball_wins": "ballons gagnés",
          "total": "total", "p90": "par 90", "poss": "par possession", "adj": "ajusté adversaire"}


def pct_in_position(df: pd.DataFrame, col: str) -> pd.Series:
    return df.groupby("position_group")[col].rank(pct=True)


def spearman(a: pd.Series, b: pd.Series) -> float:
    return a.rank().corr(b.rank())


def boot_ci(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    n, vals = len(a), []
    for _ in range(N_BOOT):
        i = RNG.integers(0, n, n)
        vals.append(pd.Series(a[i]).rank().corr(pd.Series(b[i]).rank()))
    return tuple(np.nanpercentile(vals, [2.5, 97.5]))


# ---------------------------------------------------------------- A. classements
def rank_changes(sv: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, movers = [], []
    for tname, tcol in THRESHOLDS.items():
        e = sv[sv[tcol] & (sv.position_group != "GK")].copy()
        for k in INDICATORS:
            for a, b in PAIRS:
                pa, pb = pct_in_position(e, f"{k}_{a}"), pct_in_position(e, f"{k}_{b}")
                d = pb - pa
                rows.append({
                    "seuil": tname, "n": len(e), "indicateur": k, "de": a, "vers": b,
                    "spearman": round(spearman(e[f"{k}_{a}"], e[f"{k}_{b}"]), 3),
                    "bougent_20pts": int((d.abs() >= MOVE).sum()),
                    "part_bougent": round((d.abs() >= MOVE).mean(), 3),
                    "corr_delta_possession": round(d.corr(e.team_poss_share), 2),
                })
                if tname == "5 matchs de 60 min" and (a, b) == ("p90", "poss"):
                    m = e.assign(delta_pts=(d * 100).round(1),
                                 pct_avant=(pa * 100).round(0), pct_apres=(pb * 100).round(0))
                    m = m.reindex(m.delta_pts.abs().sort_values(ascending=False).index).head(10)
                    for r in m.itertuples():
                        movers.append({"indicateur": k, "joueuse": r.player, "equipe": r.team,
                                       "poste": r.position_group, "part_possession": round(r.team_poss_share, 2),
                                       "percentile_p90": r.pct_avant, "percentile_poss": r.pct_apres,
                                       "delta_pts": r.delta_pts})
    return pd.DataFrame(rows), pd.DataFrame(movers)


# ------------------------------------------------- B. remplaçantes, faible temps de jeu
def low_minutes(sv: pd.DataFrame, pm: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    f = sv[sv.position_group != "GK"].copy()
    f["tranche"] = pd.cut(f.minutes, [0, 450, 900, np.inf], labels=["< 450 min", "450-900 min", "≥ 900 min"],
                          right=False)
    rows = []
    for k in INDICATORS:
        col = f"{k}_p90"
        f["pct"] = pct_in_position(f, col)
        top = f.groupby("position_group")[col].transform(lambda s: s >= s.quantile(0.9))
        for tr, g in f.groupby("tranche", observed=True):
            rows.append({"indicateur": k, "tranche": tr, "n": len(g),
                         "part_dans_top10_p90": round(top[g.index].mean(), 3),
                         "part_dans_top10_attendue": 0.10,
                         "ecart_type_percentile": round(g.pct.std(), 3)})
    noise = pd.DataFrame(rows)

    # Même joueuse, titulaire contre entrée en jeu (taux par 90 et part de possession)
    fm = pm[(pm.position_group != "GK") & (pm.minutes_played > 0)].copy()
    stat = fm.groupby("player_id").agg(n_start=("starter", "sum"), n=("starter", "size"))
    keep = stat[(stat.n_start >= 3) & (stat.n - stat.n_start >= 3)].index
    fm = fm[fm.player_id.isin(keep)]
    # Ratio global (Σ valeurs / Σ minutes en entrée) ÷ (même chose en titulaire), sur les mêmes
    # joueuses : évite le biais des médianes de ratios quand les entrées valent souvent 0.
    # Intervalle de confiance par bootstrap sur les joueuses.
    def pooled(g: pd.DataFrame, num: str, den: str) -> float:
        s, t = g[~g.starter], g[g.starter]
        return (s[num].sum() / s[den].sum()) / (t[num].sum() / t[den].sum())

    fm["poss_tot"] = fm.team_possession_s_on + fm.opp_possession_s_on
    players = fm.player_id.unique()
    by_player = {p: g for p, g in fm.groupby("player_id")}
    rows = []
    for k, den in [(k, "minutes_played") for k in INDICATORS + ["ball_receipts"]] + \
                  [("team_possession_s_on", "poss_tot")]:
        est = pooled(fm, k, den)
        boots = []
        for _ in range(N_BOOT):
            samp = pd.concat([by_player[p] for p in RNG.choice(players, len(players))])
            boots.append(pooled(samp, k, den))
        lo, hi = np.percentile(boots, [2.5, 97.5])
        s, t = fm[~fm.starter], fm[fm.starter]
        scale = 90 if den == "minutes_played" else 1
        rows.append({"indicateur": k if k != "team_possession_s_on" else "part_possession_equipe",
                     "joueuses": len(players),
                     "valeur_titulaire": round(t[k].sum() / t[den].sum() * scale, 3),
                     "valeur_entree": round(s[k].sum() / s[den].sum() * scale, 3),
                     "ratio_entree_sur_titulaire": round(est, 2),
                     "ic95_bas": round(lo, 2), "ic95_haut": round(hi, 2)})
    return noise, pd.DataFrame(rows)


def late_game_control(pm: pd.DataFrame, raw_dir: Path, late_minute: int = 65,
                      players=None) -> pd.DataFrame:
    """Contrôle : les titulaires qui jouent tout le match produisent-elles aussi plus en fin de match ?

    Si oui, la hausse des entrantes tient au moment du match (jeu plus ouvert, adversaires
    fatiguées), pas seulement à leur fraîcheur. Fin de match = 2e période à partir de la
    65e minute (horloge StatsBomb). Nécessite data_raw/events.
    """
    import json

    from build_indicators import match_counts

    full = pm[(pm.starter) & (pm.seconds_played >= pm.match_seconds - 1) & (pm.position_group != "GK")]
    if players is not None:
        full = full[full.player_id.isin(players)]
    keep = set(zip(full.match_id, full.player_id))
    tot = {"early": dict.fromkeys(INDICATORS, 0.0), "late": dict.fromkeys(INDICATORS, 0.0)}
    secs = {"early": 0.0, "late": 0.0}
    for mid in full.match_id.unique():
        ev = json.loads((raw_dir / "events" / f"{mid}.json").read_text())
        dur = {}
        for e in ev:
            if e["type"]["name"] == "Half End" and e["period"] <= 2:
                h, m, s = e["timestamp"].split(":")
                dur[e["period"]] = max(dur.get(e["period"], 0), int(h) * 3600 + int(m) * 60 + float(s))
        cut = (late_minute - 45) * 60
        n_players = sum(1 for (m_, _) in keep if m_ == mid)
        secs["early"] += n_players * (dur[1] + cut)
        secs["late"] += n_players * max(dur[2] - cut, 0)
        late_ev = [e for e in ev if e["period"] == 2 and e["minute"] >= late_minute]
        early_ev = [e for e in ev if e["period"] == 1 or (e["period"] == 2 and e["minute"] < late_minute)]
        # les tirs et passes clés sont rattachés à la fenêtre de l'événement
        for win, sub in (("early", early_ev), ("late", late_ev)):
            for pid, d in match_counts(sub).items():
                if (mid, pid) in keep:
                    for k in INDICATORS:
                        tot[win][k] += d[k]
    rows = []
    for k in INDICATORS:
        e90 = tot["early"][k] / secs["early"] * 5400
        l90 = tot["late"][k] / secs["late"] * 5400
        rows.append({"indicateur": k, "titulaires_match_complet": len(keep),
                     "p90_avant": round(e90, 3), "p90_fin_de_match": round(l90, 3),
                     "ratio_fin_sur_avant": round(l90 / e90, 2)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------- C. stabilité
def split_stability(pm: pd.DataFrame) -> pd.DataFrame:
    splits = {
        "aller / retour": pm.match_week <= 11,
        "matchs impairs / pairs": None,
    }
    # rang du match pour chaque joueuse (ordre chronologique) → impairs / pairs
    order = pm.sort_values("match_date").groupby(["player_id", "team_id"]).cumcount().reindex(pm.index)
    splits["matchs impairs / pairs"] = (order % 2 == 0)
    rows = []
    for sname, mask in splits.items():
        a, b = season_versions(pm[mask]), season_versions(pm[~mask])
        m = a.merge(b, on=["player_id", "team"], suffixes=("_a", "_b"))
        m = m[(m.minutes_a >= HALF_MIN) & (m.minutes_b >= HALF_MIN) & (m.position_group_a != "GK")]
        m = m.reset_index(drop=True)
        for k in INDICATORS:
            # percentiles au sein du poste, pour ne pas mesurer seulement le poste
            pc = {v: (m.groupby("position_group_a")[f"{k}_{v}_a"].rank(pct=True).to_numpy(),
                      m.groupby("position_group_a")[f"{k}_{v}_b"].rank(pct=True).to_numpy())
                  for v in ["p90", "poss", "adj"]}
            # bootstrap apparié : écart de stabilité dans le poste, version − par 90
            idx = [RNG.integers(0, len(m), len(m)) for _ in range(N_BOOT)]

            def rho(x, y, i):
                return pd.Series(x[i]).rank().corr(pd.Series(y[i]).rank())

            for v in ["p90", "poss", "adj"]:
                x, y = m[f"{k}_{v}_a"].to_numpy(), m[f"{k}_{v}_b"].to_numpy()
                lo, hi = boot_ci(x, y)
                diffs = [rho(*pc[v], i) - rho(*pc["p90"], i) for i in idx] if v != "p90" else [0.0]
                rows.append({"decoupage": sname, "n": len(m), "indicateur": k, "version": v,
                             "spearman": round(spearman(pd.Series(x), pd.Series(y)), 3),
                             "ic95_bas": round(lo, 3), "ic95_haut": round(hi, 3),
                             "spearman_dans_poste": round(spearman(pd.Series(pc[v][0]), pd.Series(pc[v][1])), 3),
                             "ecart_vs_p90_dans_poste_ic95_bas": round(np.percentile(diffs, 2.5), 3),
                             "ecart_vs_p90_dans_poste_ic95_haut": round(np.percentile(diffs, 97.5), 3)})
    return pd.DataFrame(rows)


# ------------------------------------------- D. ajustement adversaire sur demi-saison
def half_season_adjustment(pm: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for hname, mask in {"aller": pm.match_week <= 11, "retour": pm.match_week > 11}.items():
        h = pm[mask]
        faced = h.groupby("team_id").opponent_id.nunique()
        sv = season_versions(h)
        for group, sel in {"≥ 450 min": sv.minutes >= HALF_MIN,
                           "≥ 3 matchs, < 450 min": (sv.minutes < HALF_MIN) & (sv.matches >= 3)}.items():
            e = sv[sel & (sv.position_group != "GK")].copy()
            for k in INDICATORS:
                ratio = (e[f"{k}_adj"] / e[f"{k}_p90"]).replace([np.inf, -np.inf], np.nan)
                d = pct_in_position(e, f"{k}_adj") - pct_in_position(e, f"{k}_p90")
                rows.append({"moitie": hname, "adversaires_distincts_par_equipe": int(faced.min()),
                             "groupe": group, "n": len(e), "indicateur": k,
                             "ecart_adj_p90_max": round((ratio - 1).abs().max(), 3),
                             "ecart_adj_p90_median": round((ratio - 1).abs().median(), 3),
                             "bougent_20pts": int((d.abs() >= MOVE).sum())})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------- résumé
def summary_md(rc, movers, noise, subs, late, stab, adj) -> str:
    L = ["# Étape 3 — Résultats chiffrés (FA WSL 2023/24)", "",
         "Généré par `src/analyze_rankings.py`. Percentiles au sein du groupe de postes, gardiennes exclues. "
         "Data: StatsBomb.", ""]
    L += ["## A. Changements de classement (saison complète)", "",
          "| Seuil | Indicateur | Passage | ρ de Spearman | Bougent ≥ 20 pts | Lien avec la possession |",
          "|---|---|---|---|---|---|"]
    for r in rc.itertuples():
        L.append(f"| {r.seuil} (n = {r.n}) | {LABELS[r.indicateur]} | {LABELS[r.de]} → {LABELS[r.vers]} | "
                 f"{r.spearman:.2f} | {r.bougent_20pts} ({r.part_bougent:.0%}) | {r.corr_delta_possession:+.2f} |")
    L += ["", "Plus grands déplacements, par 90 → par possession (seuil 5 matchs de 60 min) :", "",
          "| Indicateur | Joueuse | Équipe | Poste | Possession | Percentile par 90 | Percentile par possession |",
          "|---|---|---|---|---|---|---|"]
    for k in INDICATORS:
        for r in movers[movers.indicateur == k].head(3).itertuples():
            L.append(f"| {LABELS[k]} | {r.joueuse} | {r.equipe} | {r.poste} | {r.part_possession:.0%} | "
                     f"{r.percentile_p90:.0f} | {r.percentile_poss:.0f} |")
    L += ["", "## B. Remplaçantes et faible temps de jeu", "",
          "Part des joueuses de chaque tranche dans le top 10 % du par 90 de leur poste (attendu : 10 %) :", "",
          "| Indicateur | < 450 min | 450-900 min | ≥ 900 min |", "|---|---|---|---|"]
    for k in INDICATORS:
        g = noise[noise.indicateur == k].set_index("tranche")
        L.append(f"| {LABELS[k]} | " + " | ".join(
            f"{g.loc[t, 'part_dans_top10_p90']:.0%} (n = {g.loc[t, 'n']})" for t in g.index) + " |")
    L += ["", "Mêmes joueuses, titulaires ou entrées en jeu (au moins 3 matchs de chaque) ; "
          "valeurs par 90 (part de possession : sans unité), ratio global entrée / titulaire et IC 95 % "
          "par bootstrap sur les joueuses :", "",
          "| Indicateur | Joueuses | Titulaire | Entrée | Ratio entrée / titulaire [IC 95 %] |",
          "|---|---|---|---|---|"]
    for r in subs.itertuples():
        lab = LABELS.get(r.indicateur, r.indicateur.replace("_", " "))
        L.append(f"| {lab} | {r.joueuses} | {r.valeur_titulaire} | {r.valeur_entree} | "
                 f"{r.ratio_entree_sur_titulaire} [{r.ic95_bas}-{r.ic95_haut}] |")
    if late is not None:
        L += ["", "Contrôle « fin de match » : les mêmes joueuses, quand elles sont titulaires et jouent tout "
              "le match, avant et après la 65e minute (par 90) :", "",
              "| Indicateur | Matchs complets | Avant la 65e | Après la 65e | Ratio fin / avant |",
              "|---|---|---|---|---|"]
        for r in late.itertuples():
            L.append(f"| {LABELS[r.indicateur]} | {r.titulaires_match_complet} | {r.p90_avant} | "
                     f"{r.p90_fin_de_match} | {r.ratio_fin_sur_avant} |")
    L += ["", f"## C. Stabilité (joueuses de champ avec au moins {HALF_MIN} min dans chaque moitié)", "",
          "ρ de Spearman entre les deux moitiés [IC 95 %] ; « poste » = même calcul sur les percentiles au sein "
          "du poste ; entre parenthèses, IC 95 % apparié de l'écart avec le par 90 au sein du poste.", "",
          "| Découpage | Indicateur | Par 90 | Par possession | Ajusté adversaire |", "|---|---|---|---|---|"]
    for (s, k), g in stab.groupby(["decoupage", "indicateur"], sort=False):
        g = g.set_index("version")
        cells = []
        for v in ["p90", "poss", "adj"]:
            c = (f"{g.loc[v, 'spearman']:.2f} [{g.loc[v, 'ic95_bas']:.2f}-{g.loc[v, 'ic95_haut']:.2f}] "
                 f"· poste {g.loc[v, 'spearman_dans_poste']:.2f}")
            if v != "p90":
                c += (f" (écart {g.loc[v, 'ecart_vs_p90_dans_poste_ic95_bas']:+.2f} à "
                      f"{g.loc[v, 'ecart_vs_p90_dans_poste_ic95_haut']:+.2f})")
            cells.append(c)
        L.append(f"| {s} (n = {g.n.iloc[0]}) | {LABELS[k]} | " + " | ".join(cells) + " |")
    L += ["", "## D. Ajustement à l'adversaire sur une demi-saison", "",
          "| Moitié | Groupe | Indicateur | Écart max adj / par 90 | Écart médian | Bougent ≥ 20 pts |",
          "|---|---|---|---|---|---|"]
    for r in adj.itertuples():
        L.append(f"| {r.moitie} ({r.adversaires_distincts_par_equipe} adversaires) | {r.groupe} (n = {r.n}) | "
                 f"{LABELS[r.indicateur]} | {r.ecart_adj_p90_max:.0%} | {r.ecart_adj_p90_median:.1%} | {r.bougent_20pts} |")
    return "\n".join(L) + "\n"


def main(proc_dir: str = "data/processed", out_dir: str = "outputs", raw_dir: str = "data_raw") -> None:
    proc, out = Path(proc_dir), Path(out_dir)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    pm = pd.read_csv(proc / "player_match_indicators_wsl_2324.csv")
    sv = pd.read_csv(proc / "player_season_versions_wsl_2324.csv")
    rc, movers = rank_changes(sv)
    noise, subs = low_minutes(sv, pm)
    raw = Path(raw_dir) / "events"
    late = None
    if raw.exists():
        f = pm[pm.position_group != "GK"]
        st = f.groupby("player_id").agg(a=("starter", "sum"), n=("starter", "size"))
        rotation = st[(st.a >= 3) & (st.n - st.a >= 3)].index
        late = late_game_control(pm, Path(raw_dir), players=rotation)
    else:
        print(f"{raw} absent : contrôle « fin de match » non calculé (lancer src/download.py)")
    stab = split_stability(pm)
    adj = half_season_adjustment(pm)
    tables = {"changements_classement": rc, "plus_grands_deplacements": movers,
              "faible_temps_de_jeu": noise, "titulaire_contre_entree": subs,
              "stabilite": stab, "ajustement_demi_saison": adj}
    if late is not None:
        tables["controle_fin_de_match"] = late
    for name, df in tables.items():
        df.to_csv(out / "tables" / f"{name}.csv", index=False)
    (out / "resultats_etape3.md").write_text(summary_md(rc, movers, noise, subs, late, stab, adj),
                                             encoding="utf-8")
    print(f"Étape 3 : {len(tables)} tables dans {out / 'tables'} et résumé {out / 'resultats_etape3.md'}")


if __name__ == "__main__":
    main(*sys.argv[1:])
