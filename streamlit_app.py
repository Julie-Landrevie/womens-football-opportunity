"""Comparer les joueuses à opportunités égales — application Streamlit (français / anglais, clair / sombre).

Lancer : streamlit run streamlit_app.py
Données : data/processed/player_season_versions_all_2324.csv et outputs/comparaison/tables/
(produits par les scripts de src/). Data: StatsBomb.
"""
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from jl_ui import C, altair_style, footer, fr_num, header, kpi, setup, t

ROOT = Path(__file__).resolve().parent

setup("Comparer à opportunités égales", "Comparing on equal opportunities", icon="⚽")

INDICATORS = {"npxg": ("xG hors penalties", "Non-penalty xG"),
              "xa": ("xA (passes avant un tir)", "xA (passes leading to a shot)"),
              "prog": ("Actions progressives", "Progressive actions"),
              "pressures": ("Pressions", "Pressures"),
              "ball_wins": ("Ballons gagnés", "Ball wins")}
SHORT = {"npxg": ("xG hors penalties", "non-penalty xG"), "xa": ("xA", "xA"),
         "prog": ("actions progressives", "progressive actions"), "pressures": ("pressions", "pressures"),
         "ball_wins": ("ballons gagnés", "ball wins")}
DEFENSIVE = {"pressures", "ball_wins"}
VERSIONS = {"total": ("Total saison", "Season total"), "p90": ("Par 90 minutes", "Per 90 minutes"),
            "poss": ("Par possession", "Per possession"), "adj": ("Ajusté adversaire", "Opponent-adjusted")}
POSITIONS = {"CB": ("Défenseures centrales", "Centre-backs"), "FB": ("Latérales", "Full-backs"),
             "DM": ("Milieux défensives", "Defensive midfielders"), "CM": ("Milieux centrales", "Central midfielders"),
             "AM": ("Milieux offensives", "Attacking midfielders"), "W": ("Ailières", "Wingers"),
             "FW": ("Attaquantes", "Forwards")}
THRESHOLDS = {"eligible_5x60": ("Au moins 5 matchs de 60 min (seuil SkillCorner)", "At least 5 matches of 60 min (SkillCorner threshold)"),
              "eligible_900": ("Au moins 900 minutes", "At least 900 minutes")}
LEAGUE_ORDER = ["FA WSL", "Frauen-Bundesliga", "Liga F", "Serie A Women"]
ALL = "__all__"


def L(d: dict, k: str) -> str:
    return t(*d[k])


def version_help(k: str, v: str) -> str:
    if v == "poss":
        return (t("par 30 min de possession adverse", "per 30 min of opponent possession") if k in DEFENSIVE
                else t("par 30 min de possession de l’équipe", "per 30 min of team possession"))
    return {"total": t("sur la saison", "over the season"), "p90": t("par 90 minutes jouées", "per 90 minutes played"),
            "adj": t("par 90 minutes, ajusté au niveau des adversaires affrontés",
                     "per 90 minutes, adjusted for the opponents faced")}[v]


@st.cache_data
def load_players() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data/processed/player_season_versions_all_2324.csv")


@st.cache_data
def load_table(name: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / "outputs/comparaison/tables" / f"{name}.csv")


def percentiles(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[f"pct_{c}"] = out.groupby("position_group")[c].rank(pct=True) * 100
    return out


players = load_players()

with st.sidebar:
    st.markdown(f"### {t('Sélection', 'Selection')}")
    league = st.selectbox(t("Championnat (2023/24)", "League (2023/24)"), [ALL] + LEAGUE_ORDER,
                          format_func=lambda x: t("Les 4 championnats", "All 4 leagues") if x == ALL else x)
    pos = st.selectbox(t("Poste", "Position"), list(POSITIONS), format_func=lambda k: L(POSITIONS, k),
                       index=list(POSITIONS).index("CM"))
    ind = st.selectbox(t("Indicateur", "Indicator"), list(INDICATORS), format_func=lambda k: L(INDICATORS, k),
                       index=list(INDICATORS).index("pressures"))
    v_from = st.selectbox(t("Comparer…", "Compare…"), list(VERSIONS), format_func=lambda k: L(VERSIONS, k), index=1)
    others = [v for v in VERSIONS if v != v_from]
    v_to = st.selectbox(t("… avec", "… with"), others, format_func=lambda k: L(VERSIONS, k),
                        index=others.index("poss") if "poss" in others else 0)
    thr = st.radio(t("Joueuses retenues", "Players included"), list(THRESHOLDS), format_func=lambda k: L(THRESHOLDS, k))
    st.caption(t("Percentiles calculés au sein du poste, parmi les joueuses retenues",
                 "Percentiles computed within position, among the players included")
               + (t(" des quatre championnats réunis (sans correction du niveau de chaque championnat).",
                    " of all four leagues pooled (no adjustment for league strength).") if league == ALL
                  else t(f" de {league}.", f" of {league}.")))

header(t("Comparer à opportunités égales", "Comparing on equal opportunities"),
       t("Le classement d’une joueuse change-t-il quand on tient compte de ses opportunités : temps de jeu, possession "
         "de son équipe, adversaires ? Football féminin, quatre championnats 2023/24, données StatsBomb.",
         "Does a player’s ranking change once her opportunities are taken into account: playing time, team "
         "possession, opponents? Women’s football, four 2023/24 leagues, StatsBomb data."))

tab_rank, tab_player, tab_sub, tab_method = st.tabs(
    [t("Classements", "Rankings"), t("Fiche joueuse", "Player card"), t("Entrer en jeu", "Coming off the bench"),
     t("Méthode et limites", "Method and limits")])

sel = players[(players.position_group != "GK") & players[thr]]
if league != ALL:
    sel = sel[sel.league_name == league]
col_a, col_b = f"{ind}_{v_from}", f"{ind}_{v_to}"
name_a, name_b = L(VERSIONS, v_from), L(VERSIONS, v_to)

# ------------------------------------------------------------------------- classements
with tab_rank:
    p = percentiles(sel, [col_a, col_b])
    g = p[p.position_group == pos].copy()
    g["delta"] = g[f"pct_{col_b}"] - g[f"pct_{col_a}"]
    moved_all = (p[f"pct_{col_b}"] - p[f"pct_{col_a}"]).abs() >= 20
    rho = p[col_a].rank().corr(p[col_b].rank())

    c1, c2, c3 = st.columns(3)
    kpi(c1, str(len(g)), t(f"{L(POSITIONS, pos).lower()} retenues", f"{L(POSITIONS, pos).lower()} included"))
    kpi(c2, fr_num(moved_all.mean() * 100, 0, pct=True),
        t("des joueuses (tous postes) bougent d’au moins 20 points de percentile",
          "of players (all positions) move by at least 20 percentile points"), accent=True)
    kpi(c3, fr_num(rho, 2), t(f"corrélation de rang entre « {name_a.lower()} » et « {name_b.lower()} »",
                              f"rank correlation between “{name_a.lower()}” and “{name_b.lower()}”"))

    st.markdown(f"### {L(INDICATORS, ind)}{t(' :', ':')} {name_a.lower()} {t('contre', 'vs')} {name_b.lower()}")
    st.caption(t(f"Chaque point est une joueuse. Sur la diagonale, son rang ne change pas ; au-dessus, elle gagne des "
                 f"places quand on passe de « {version_help(ind, v_from)} » à « {version_help(ind, v_to)} ». "
                 "Couleur : part de possession de son équipe pendant qu’elle était sur le terrain.",
                 f"Each dot is a player. On the diagonal her rank does not change; above it, she gains places when "
                 f"moving from “{version_help(ind, v_from)}” to “{version_help(ind, v_to)}”. "
                 "Colour: her team’s share of possession while she was on the pitch."))
    if len(g) < 5:
        st.info(t("Trop peu de joueuses pour ce poste avec cette sélection.", "Too few players for this position with this selection."))
    else:
        g["equipe_possession"] = (g.team_poss_share * 100).round(0)
        g["pa"] = g[f"pct_{col_a}"].round(0)
        g["pb"] = g[f"pct_{col_b}"].round(0)
        poss_t = t("Possession de l’équipe (%)", "Team possession (%)")
        diag = alt.Chart(pd.DataFrame({"x": [0, 100], "y": [0, 100]})).mark_line(
            color=C["compare"], strokeDash=[4, 4]).encode(x="x", y="y")
        pts = alt.Chart(g).mark_circle(size=110, opacity=0.9).encode(
            x=alt.X("pa:Q", title=t("Percentile — ", "Percentile — ") + name_a.lower(), scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("pb:Q", title=t("Percentile — ", "Percentile — ") + name_b.lower(), scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("equipe_possession:Q", title=poss_t, scale=alt.Scale(range=[C["compare"], C["teal"]])),
            tooltip=[alt.Tooltip("player:N", title=t("Joueuse", "Player")), alt.Tooltip("team:N", title=t("Équipe", "Team")),
                     alt.Tooltip("league_name:N", title=t("Championnat", "League")),
                     alt.Tooltip("minutes:Q", title="Minutes", format=".0f"),
                     alt.Tooltip("equipe_possession:Q", title=poss_t),
                     alt.Tooltip("pa:Q", title=name_a), alt.Tooltip("pb:Q", title=name_b)])
        st.altair_chart(altair_style((diag + pts).properties(height=480)), width="stretch", theme="streamlit")

        show = ["player", "team", "league_name", "minutes", "team_poss_share", col_a, f"pct_{col_a}",
                col_b, f"pct_{col_b}", "delta"]
        pct1, pct2 = t("Percentile", "Percentile"), t("Percentile ", "Percentile ")
        names = {"player": t("Joueuse", "Player"), "team": t("Équipe", "Team"), "league_name": t("Championnat", "League"),
                 "minutes": "Minutes", "team_poss_share": t("Possession équipe", "Team possession"), col_a: name_a,
                 f"pct_{col_a}": pct1, col_b: name_b, f"pct_{col_b}": pct2, "delta": t("Écart (points)", "Change (points)")}
        fmt = {"Minutes": "{:.0f}", names["team_poss_share"]: "{:.0%}", name_a: "{:.2f}", pct1: "{:.0f}",
               name_b: "{:.2f}", pct2: "{:.0f}", names["delta"]: "{:+.0f}"}
        up, down = st.columns(2)
        with up:
            st.markdown(f"**{t('Gagnent le plus de places', 'Gain the most places')}**")
            st.dataframe(g.nlargest(8, "delta")[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")
        with down:
            st.markdown(f"**{t('Perdent le plus de places', 'Lose the most places')}**")
            st.dataframe(g.nsmallest(8, "delta")[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")
        with st.expander(t(f"Classement complet des {L(POSITIONS, pos).lower()} ({len(g)})",
                           f"Full ranking of {L(POSITIONS, pos).lower()} ({len(g)})")):
            st.dataframe(g.sort_values(col_b, ascending=False)[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")

# ------------------------------------------------------------------------ fiche joueuse
with tab_player:
    pool = percentiles(sel, [f"{k}_{v}" for k in INDICATORS for v in VERSIONS])
    cand = pool[pool.position_group == pos].sort_values("minutes", ascending=False)
    if cand.empty:
        st.info(t("Aucune joueuse pour cette sélection.", "No player for this selection."))
    else:
        labels = {i: f"{r.player} — {r.team} ({r.league_name})" for i, r in cand.iterrows()}
        who = st.selectbox(t(f"Joueuse ({L(POSITIONS, pos).lower()}, triées par minutes)",
                             f"Player ({L(POSITIONS, pos).lower()}, sorted by minutes)"), list(labels),
                           format_func=labels.get)
        r = cand.loc[who]
        c1, c2, c3, c4 = st.columns(4)
        kpi(c1, fr_num(r.minutes, 0), t("minutes jouées", "minutes played"))
        kpi(c2, f"{int(r.starts)} / {int(r.matches)}", t("titularisations / matchs", "starts / matches"))
        kpi(c3, fr_num(r.team_poss_share * 100, 0, pct=True), t("possession de son équipe quand elle joue",
                                                               "her team’s possession when she plays"))
        kpi(c4, fr_num(r[f"{ind}_{v_to}"], 2), f"{L(SHORT, ind)} — {name_b.lower()}")
        st.markdown(f"### {t('Percentiles parmi les', 'Percentiles among')} {L(POSITIONS, pos).lower()} : "
                    f"{name_a.lower()} {t('contre', 'vs')} {name_b.lower()}")
        rows = []
        for k in INDICATORS:
            for v in (v_from, v_to):
                rows.append({"ind": L(INDICATORS, k), "ver": L(VERSIONS, v), "pct": round(r[f"pct_{k}_{v}"], 0)})
        order = [L(INDICATORS, k) for k in INDICATORS]
        bars = alt.Chart(pd.DataFrame(rows)).mark_bar(height=14, cornerRadiusEnd=3).encode(
            y=alt.Y("ind:N", sort=order, title=None),
            yOffset=alt.YOffset("ver:N", sort=[name_a, name_b]),
            x=alt.X("pct:Q", scale=alt.Scale(domain=[0, 100]), title=t("Percentile au sein du poste", "Percentile within position")),
            color=alt.Color("ver:N", sort=[name_a, name_b], scale=alt.Scale(range=[C["compare"], C["teal"]]),
                            legend=alt.Legend(orient="top", title=None)),
            tooltip=[alt.Tooltip("ind:N", title=t("Indicateur", "Indicator")), alt.Tooltip("ver:N", title="Version"),
                     alt.Tooltip("pct:Q", title="Percentile")])
        st.altair_chart(altair_style(bars.properties(height=330)), width="stretch", theme="streamlit")
        st.caption(t("Gris : première version choisie ; vert d’eau : seconde. Changer les versions dans le menu de gauche.",
                     "Grey: first version chosen; teal: second. Change the versions in the left menu."))

# ----------------------------------------------------------------------- entrer en jeu
with tab_sub:
    st.markdown(f"### {t('Une remplaçante produit plus par minute que la même joueuse titulaire', 'A substitute produces more per minute than the same player as a starter')}")
    st.markdown(t(
        "Le par 90 compare des minutes qui ne se valent pas. Pour le vérifier sans mélanger les joueuses ni les "
        "moments du match, on compare **chaque joueuse à elle-même** : ses matchs où elle entre à partir de la 65e "
        "minute, contre ses matchs complets **sur la même fenêtre** (65e minute → fin). 200 joueuses de champ des "
        "quatre championnats, au moins 3 matchs de chaque.",
        "Per-90 figures compare minutes that are not alike. To check it without mixing players or match phases, "
        "**each player is compared with herself**: matches where she comes on from the 65th minute, against her "
        "full matches **over the same window** (65th minute → end). 200 outfield players from the four leagues, "
        "at least 3 matches of each."))
    sw = load_table("meme_fenetre")
    pooled = sw[sw.perimetre == "4 ligues"].set_index("indicateur")
    cols = st.columns(len(INDICATORS))
    for c, k in zip(cols, INDICATORS):
        r = pooled.loc[k]
        kpi(c, "×" + fr_num(r.ratio, 2), f"{L(SHORT, k)}<br>{t('IC 95 %', '95% CI')} {fr_num(r.ic95_bas, 2)} "
            f"{t('à', 'to')} {fr_num(r.ic95_haut, 2)}", accent=(k == "pressures"))
    k_sel = st.selectbox(t("Indicateur à détailler par championnat", "Indicator to break down by league"),
                         list(INDICATORS), format_func=lambda k: L(INDICATORS, k),
                         index=list(INDICATORS).index("pressures"), key="k_sub")
    d = sw[sw.indicateur == k_sel].copy()
    pooled_name = t("4 championnats réunis", "All 4 leagues pooled")
    d["perim"] = d.perimetre.replace({"4 ligues": pooled_name})
    order = [pooled_name] + LEAGUE_ORDER
    base = alt.Chart(d).encode(y=alt.Y("perim:N", sort=order, title=None))
    rule = base.mark_rule(color=C["compare"], strokeWidth=3).encode(
        x=alt.X("ic95_bas:Q", title=t("Ratio entrée tardive / titulaire (même fenêtre)",
                                       "Late substitute / starter ratio (same window)"),
                scale=alt.Scale(zero=False, nice=False, domain=[min(0.8, d.ic95_bas.min() - 0.05), d.ic95_haut.max() + 0.05])),
        x2="ic95_haut:Q")
    dots = base.mark_circle(size=160).encode(
        x="ratio:Q",
        color=alt.condition(alt.datum.perim == pooled_name, alt.value(C["rust"]), alt.value(C["teal"])),
        tooltip=[alt.Tooltip("perim:N", title=t("Périmètre", "Scope")), alt.Tooltip("joueuses:Q", title=t("Joueuses", "Players")),
                 alt.Tooltip("ratio:Q", title="Ratio"), alt.Tooltip("ic95_bas:Q", title=t("IC bas", "CI low")),
                 alt.Tooltip("ic95_haut:Q", title=t("IC haut", "CI high"))])
    one = alt.Chart(pd.DataFrame({"x": [1]})).mark_rule(color=C["muted"], strokeDash=[4, 4]).encode(x="x:Q")
    st.altair_chart(altair_style((rule + dots + one).properties(height=260)), width="stretch", theme="streamlit")
    st.caption(t("Point : ratio global ; trait : intervalle de confiance à 95 % (bootstrap sur les joueuses). "
                 "À droite de la ligne pointillée, la joueuse produit plus en entrant qu’en jouant tout le match. "
                 "Les championnats seuls comptent 26 à 101 joueuses : intervalles plus larges.",
                 "Dot: overall ratio; line: 95% confidence interval (bootstrap over players). Right of the dashed "
                 "line, the player produces more when coming on than when playing the full match. Single leagues "
                 "have 26 to 101 players: wider intervals."))
    st.markdown(t(
        "**Ce que ça change** : le par 90 d’une remplaçante surestime ce qu’elle ferait sur un match entier, "
        "surtout pour le pressing. Pour comparer une remplaçante et une titulaire, regarder la même fenêtre de "
        "match, ou au moins le signaler. **Ce que ça ne dit pas** : pourquoi (fraîcheur, consigne du staff, état "
        "du score) ; la part de possession de l’équipe, elle, est la même dans les deux cas.",
        "**What it changes**: a substitute’s per-90 figure overstates what she would do over a full match, "
        "especially for pressing. To compare a substitute with a starter, look at the same match window, or at "
        "least flag it. **What it does not say**: why (freshness, staff instructions, game state); the team’s "
        "share of possession is the same in both cases."))

# -------------------------------------------------------------------- méthode et limites
with tab_method:
    st.markdown(t("""
### Données
StatsBomb Open Data, quatre championnats féminins 2023/24 : FA WSL (132 matchs), Frauen-Bundesliga (132), Liga F (240),
Serie A Women (130). Joueuses de champ seulement ; gardiennes exclues.

### Opportunités mesurées
- **Temps de jeu** reconstruit à partir des événements (remplacements, expulsions), car les horaires des feuilles de match
  sont faux dans plusieurs matchs.
- **Possession pendant la présence** : du premier au dernier événement de jeu de chaque possession, événements
  administratifs exclus (environ 52 à 57 minutes par match selon le championnat).
- **Niveau des adversaires** : ce que les autres équipes produisent contre chaque adversaire, rapporté à la moyenne du
  championnat (l’équipe de la joueuse est exclue du calcul).

### Les quatre versions
- **Total saison** : somme brute ; mesure d’abord le temps de jeu.
- **Par 90 minutes** : la référence habituelle.
- **Par possession** : offensif par 30 minutes de possession de l’équipe, défensif par 30 minutes de possession adverse.
  Principe repris des indicateurs TIP / OTIP de **SkillCorner** (analyses de Victoria Friss de Kereki), adapté ici à des
  données d’événements.
- **Ajusté adversaire** : par 90, divisé par le niveau moyen des adversaires affrontés.

### Ce qu’on retient
- La normalisation par possession reclasse environ **un tiers des joueuses** en pressions, dans les quatre championnats,
  en fonction de la domination de leur équipe ; presque rien en offensif.
- L’ajustement à l’adversaire ne déplace presque personne, même en Serie A où le calendrier est déséquilibré (poules).
- Une remplaçante presse **un tiers de plus** par minute que la même joueuse titulaire, sur la même fenêtre de match.

### Limites
- Données d’événements : les courses sans ballon et l’intensité physique ne sont pas mesurées (SkillCorner, lui,
  travaille sur du tracking).
- Une saison par championnat ; percentiles « 4 championnats » sans correction du niveau de chaque championnat.
- Une version moins stable d’une moitié de saison à l’autre n’est pas une moins bonne mesure : le par 90 garde une part de
  style d’équipe qui ne change pas.
- Les ajustements sont des modèles : ils réduisent un biais, ils ne donnent pas une « vraie » valeur.

Idée de départ : Bozděch (2026, *PLOS ONE*, doi 10.1371/journal.pone.0359538), mesurer la performance selon les
opportunités de l’exprimer. Code : [github.com/Julie-Landrevie/womens-football-opportunity](https://github.com/Julie-Landrevie/womens-football-opportunity).
""", """
### Data
StatsBomb Open Data, four 2023/24 women’s leagues: FA WSL (132 matches), Frauen-Bundesliga (132), Liga F (240),
Serie A Women (130). Outfield players only; goalkeepers excluded.

### Opportunities measured
- **Playing time** rebuilt from events (substitutions, red cards), because line-up timings are wrong in several matches.
- **Possession while on the pitch**: from the first to the last on-ball event of each possession, administrative events
  excluded (about 52 to 57 minutes per match depending on the league).
- **Opponent strength**: what the other teams produce against each opponent, relative to the league average (the
  player’s own team is left out of the calculation).

### The four versions
- **Season total**: raw sum; mostly measures playing time.
- **Per 90 minutes**: the usual reference.
- **Per possession**: attacking actions per 30 minutes of team possession, defensive actions per 30 minutes of opponent
  possession. The idea comes from **SkillCorner**’s TIP / OTIP metrics (analyses by Victoria Friss de Kereki), adapted
  here to event data.
- **Opponent-adjusted**: per 90, divided by the average strength of the opponents faced.

### Key takeaways
- Possession normalisation reranks about **one player in three** in pressures, in all four leagues, according to how
  dominant her team is; almost nothing in attack.
- Opponent adjustment barely moves anyone, even in Serie A with its unbalanced schedule (end-of-season pools).
- A substitute presses **a third more** per minute than the same player as a starter, over the same match window.

### Limits
- Event data: off-ball runs and physical intensity are not measured (SkillCorner works with tracking data).
- One season per league; “all 4 leagues” percentiles do not adjust for league strength.
- A version that is less stable from one half-season to the next is not a worse measure: per-90 figures keep part of a
  team style that does not change.
- Adjustments are models: they reduce a bias, they do not give a “true” value.

Starting idea: Bozděch (2026, *PLOS ONE*, doi 10.1371/journal.pone.0359538), measuring performance according to the
opportunities to express it. Code: [github.com/Julie-Landrevie/womens-football-opportunity](https://github.com/Julie-Landrevie/womens-football-opportunity).
"""))

footer("Data: StatsBomb (Open Data) · Normalisation par possession inspirée de SkillCorner",
       "Data: StatsBomb (Open Data) · Possession normalisation inspired by SkillCorner")
