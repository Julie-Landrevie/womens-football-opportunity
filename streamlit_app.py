"""Comparer les joueuses à opportunités égales — application Streamlit.

Lancer : streamlit run streamlit_app.py
Données : data/processed/player_season_versions_all_2324.csv et outputs/comparaison/tables/
(produits par les scripts de src/). Data: StatsBomb.
"""
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
C = dict(bg="#f6f1e7", ink="#1c1917", ink2="#57534e", muted="#8a8580", grid="#e4dccd",
         teal="#0d8f84", rust="#cc4a12", compare="#c9c0b1", card="#fbf8f2")

INDICATORS = {"npxg": "xG hors penalties", "xa": "xA (passes avant un tir)", "prog": "Actions progressives",
              "pressures": "Pressions", "ball_wins": "Ballons gagnés"}
DEFENSIVE = {"pressures", "ball_wins"}
VERSIONS = {"total": "Total saison", "p90": "Par 90 minutes", "poss": "Par possession", "adj": "Ajusté adversaire"}
POSITIONS = {"CB": "Défenseures centrales", "FB": "Latérales", "DM": "Milieux défensives", "CM": "Milieux centrales",
             "AM": "Milieux offensives", "W": "Ailières", "FW": "Attaquantes"}
THRESHOLDS = {"eligible_5x60": "Au moins 5 matchs de 60 min (seuil SkillCorner)",
              "eligible_900": "Au moins 900 minutes"}
LEAGUE_ORDER = ["FA WSL", "Frauen-Bundesliga", "Liga F", "Serie A Women"]
SHORT = {"npxg": "xG hors penalties", "xa": "xA", "prog": "actions progressives", "pressures": "pressions",
         "ball_wins": "ballons gagnés"}
FONT = "Lato, 'Helvetica Neue', Arial, sans-serif"
FR_NUM = "replace(format(datum.value, '.1f'), '.', ',')"


def fr(x: float, dec: int = 1, pct: bool = False) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s + (" %" if pct else "")


def version_help(k: str, v: str) -> str:
    if v == "poss":
        return ("par 30 min de possession adverse" if k in DEFENSIVE else "par 30 min de possession de l’équipe")
    return {"total": "sur la saison", "p90": "par 90 minutes jouées",
            "adj": "par 90 minutes, ajusté au niveau des adversaires affrontés"}[v]


@st.cache_data
def load_players() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data/processed/player_season_versions_all_2324.csv")


@st.cache_data
def load_table(name: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / "outputs/comparaison/tables" / f"{name}.csv")


def style() -> None:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Lato:wght@400;700;900&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, label, input, button, .stSelectbox, .stRadio {{
  font-family: 'Lato', sans-serif; }}
h1, h2, h3 {{ font-family: 'DM Serif Display', serif !important; font-weight: 400 !important; color: {C['ink']}; }}
h1 {{ font-size: 2.4rem !important; line-height: 1.1 !important; }}
.jl-sub {{ color: {C['ink2']}; font-size: 1.05rem; margin-top: -0.4rem; }}
.jl-kpi {{ background: {C['card']}; border: 1px solid {C['grid']}; border-radius: 10px; padding: 0.9rem 1rem; }}
.jl-kpi .v {{ font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: {C['ink']}; line-height: 1.1; }}
.jl-kpi .l {{ color: {C['ink2']}; font-size: 0.9rem; }}
.jl-foot {{ color: {C['ink2']}; font-size: 0.85rem; border-top: 1px solid {C['grid']}; margin-top: 2rem; padding-top: 0.8rem;
  display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }}
.jl-mono {{ display: inline-block; border: 2px solid {C['teal']}; border-radius: 6px; color: {C['teal']};
  font-weight: 700; padding: 0 0.4rem; margin-left: 0.4rem; }}
</style>""", unsafe_allow_html=True)


def kpi(col, value: str, label: str) -> None:
    col.markdown(f'<div class="jl-kpi"><div class="v">{value}</div><div class="l">{label}</div></div>',
                 unsafe_allow_html=True)


def axis_cfg(chart: alt.Chart) -> alt.Chart:
    return (chart.configure(background=C["bg"], font=FONT)
            .configure_view(stroke=None)
            .configure_axis(grid=True, gridColor=C["grid"], domain=False, ticks=False, tickCount=5,
                            labelFont=FONT, titleFont=FONT, labelColor=C["ink2"], titleColor=C["ink2"],
                            labelFontSize=12, titleFontSize=13, titleFontWeight="normal", labelLimit=260)
            .configure_legend(labelFont=FONT, titleFont=FONT, labelColor=C["ink2"], titleColor=C["ink2"],
                              titleFontWeight="normal", labelFontSize=12, titleFontSize=12))


def percentiles(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[f"pct_{c}"] = out.groupby("position_group")[c].rank(pct=True) * 100
    return out


# ----------------------------------------------------------------------------- page
st.set_page_config(page_title="Comparer à opportunités égales", page_icon="⚽", layout="wide")
style()
players = load_players()

with st.sidebar:
    st.markdown("### Sélection")
    league = st.selectbox("Championnat (2023/24)", ["Les 4 championnats"] + LEAGUE_ORDER)
    pos = st.selectbox("Poste", list(POSITIONS), format_func=POSITIONS.get, index=list(POSITIONS).index("CM"))
    ind = st.selectbox("Indicateur", list(INDICATORS), format_func=INDICATORS.get,
                       index=list(INDICATORS).index("pressures"))
    v_from = st.selectbox("Comparer…", list(VERSIONS), format_func=VERSIONS.get, index=1)
    v_to = st.selectbox("… avec", [v for v in VERSIONS if v != v_from], format_func=VERSIONS.get,
                        index=[v for v in VERSIONS if v != v_from].index("poss") if v_from != "poss" else 0)
    thr = st.radio("Joueuses retenues", list(THRESHOLDS), format_func=THRESHOLDS.get)
    st.caption("Percentiles calculés au sein du poste, parmi les joueuses retenues"
               + (" des quatre championnats réunis (sans correction du niveau de chaque championnat)."
                  if league == "Les 4 championnats" else f" de {league}."))

st.markdown("# Comparer à opportunités égales")
st.markdown('<p class="jl-sub">Le classement d’une joueuse change-t-il quand on tient compte de ses opportunités : '
            'temps de jeu, possession de son équipe, adversaires&nbsp;? Football féminin, quatre championnats '
            '2023/24, données StatsBomb.</p>', unsafe_allow_html=True)

tab_rank, tab_player, tab_sub, tab_method = st.tabs(
    ["Classements", "Fiche joueuse", "Entrer en jeu", "Méthode et limites"])

sel = players[(players.position_group != "GK") & players[thr]]
if league != "Les 4 championnats":
    sel = sel[sel.league_name == league]
col_a, col_b = f"{ind}_{v_from}", f"{ind}_{v_to}"

# ------------------------------------------------------------------------- classements
with tab_rank:
    p = percentiles(sel, [col_a, col_b])
    g = p[p.position_group == pos].copy()
    g["delta"] = g[f"pct_{col_b}"] - g[f"pct_{col_a}"]
    moved_all = (p[f"pct_{col_b}"] - p[f"pct_{col_a}"]).abs() >= 20
    rho = p[col_a].rank().corr(p[col_b].rank())

    c1, c2, c3 = st.columns(3)
    kpi(c1, str(len(g)), f"{POSITIONS[pos].lower()} retenues")
    kpi(c2, fr(moved_all.mean() * 100, 0, pct=True),
        f"des joueuses (tous postes) bougent d’au moins 20 points de percentile")
    kpi(c3, fr(rho, 2), f"corrélation de rang entre « {VERSIONS[v_from].lower()} » et « {VERSIONS[v_to].lower()} »")

    st.markdown(f"### {INDICATORS[ind]} : {VERSIONS[v_from].lower()} contre {VERSIONS[v_to].lower()}")
    st.caption(f"Chaque point est une joueuse. Sur la diagonale, son rang ne change pas ; au-dessus, elle gagne des "
               f"places quand on passe de « {version_help(ind, v_from)} » à « {version_help(ind, v_to)} ». "
               "Couleur : part de possession de son équipe pendant qu’elle était sur le terrain.")
    if len(g) < 5:
        st.info("Trop peu de joueuses pour ce poste avec cette sélection.")
    else:
        g["equipe_possession"] = (g.team_poss_share * 100).round(0)
        g["pa"] = g[f"pct_{col_a}"].round(0)
        g["pb"] = g[f"pct_{col_b}"].round(0)
        diag = alt.Chart(pd.DataFrame({"x": [0, 100], "y": [0, 100]})).mark_line(
            color=C["compare"], strokeDash=[4, 4]).encode(x="x", y="y")
        pts = alt.Chart(g).mark_circle(size=110, opacity=0.9, stroke=C["bg"], strokeWidth=1).encode(
            x=alt.X("pa:Q", title=f"Percentile — {VERSIONS[v_from].lower()}", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("pb:Q", title=f"Percentile — {VERSIONS[v_to].lower()}", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("equipe_possession:Q", title="Possession de l’équipe (%)",
                            scale=alt.Scale(range=[C["compare"], C["teal"]])),
            tooltip=[alt.Tooltip("player:N", title="Joueuse"), alt.Tooltip("team:N", title="Équipe"),
                     alt.Tooltip("league_name:N", title="Championnat"),
                     alt.Tooltip("minutes:Q", title="Minutes", format=".0f"),
                     alt.Tooltip("equipe_possession:Q", title="Possession de l’équipe (%)"),
                     alt.Tooltip("pa:Q", title=VERSIONS[v_from]), alt.Tooltip("pb:Q", title=VERSIONS[v_to])])
        st.altair_chart(axis_cfg((diag + pts).properties(height=480)), width="stretch")

        show = ["player", "team", "league_name", "minutes", "team_poss_share", col_a, f"pct_{col_a}",
                col_b, f"pct_{col_b}", "delta"]
        names = {"player": "Joueuse", "team": "Équipe", "league_name": "Championnat", "minutes": "Minutes",
                 "team_poss_share": "Possession équipe", col_a: VERSIONS[v_from], f"pct_{col_a}": "Percentile",
                 col_b: VERSIONS[v_to], f"pct_{col_b}": "Percentile ", "delta": "Écart (points)"}
        fmt = {"Minutes": "{:.0f}", "Possession équipe": "{:.0%}", VERSIONS[v_from]: "{:.2f}",
               "Percentile": "{:.0f}", VERSIONS[v_to]: "{:.2f}", "Percentile ": "{:.0f}", "Écart (points)": "{:+.0f}"}
        up, down = st.columns(2)
        with up:
            st.markdown("**Gagnent le plus de places**")
            st.dataframe(g.nlargest(8, "delta")[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")
        with down:
            st.markdown("**Perdent le plus de places**")
            st.dataframe(g.nsmallest(8, "delta")[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")
        with st.expander(f"Classement complet des {POSITIONS[pos].lower()} ({len(g)})"):
            st.dataframe(g.sort_values(col_b, ascending=False)[show].rename(columns=names).style.format(fmt),
                         hide_index=True, width="stretch")

# ------------------------------------------------------------------------ fiche joueuse
with tab_player:
    pool = percentiles(sel, [f"{k}_{v}" for k in INDICATORS for v in VERSIONS])
    cand = pool[pool.position_group == pos].sort_values("minutes", ascending=False)
    if cand.empty:
        st.info("Aucune joueuse pour cette sélection.")
    else:
        labels = {i: f"{r.player} — {r.team} ({r.league_name})" for i, r in cand.iterrows()}
        who = st.selectbox(f"Joueuse ({POSITIONS[pos].lower()}, triées par minutes)", list(labels),
                           format_func=labels.get)
        r = cand.loc[who]
        c1, c2, c3, c4 = st.columns(4)
        kpi(c1, fr(r.minutes, 0), "minutes jouées")
        kpi(c2, f"{int(r.starts)} / {int(r.matches)}", "titularisations / matchs")
        kpi(c3, fr(r.team_poss_share * 100, 0, pct=True), "possession de son équipe quand elle joue")
        kpi(c4, fr(r[f"{ind}_{v_to}"], 2), f"{SHORT[ind]} — {VERSIONS[v_to].lower()}")
        st.markdown(f"### Percentiles parmi les {POSITIONS[pos].lower()} : {VERSIONS[v_from].lower()} contre "
                    f"{VERSIONS[v_to].lower()}")
        rows = []
        for k, lab in INDICATORS.items():
            for v in (v_from, v_to):
                rows.append({"Indicateur": lab, "Version": VERSIONS[v], "Percentile": round(r[f"pct_{k}_{v}"], 0)})
        bars = alt.Chart(pd.DataFrame(rows)).mark_bar(height=14, cornerRadiusEnd=3).encode(
            y=alt.Y("Indicateur:N", sort=list(INDICATORS.values()), title=None),
            yOffset=alt.YOffset("Version:N", sort=[VERSIONS[v_from], VERSIONS[v_to]]),
            x=alt.X("Percentile:Q", scale=alt.Scale(domain=[0, 100]), title="Percentile au sein du poste"),
            color=alt.Color("Version:N", sort=[VERSIONS[v_from], VERSIONS[v_to]],
                            scale=alt.Scale(range=[C["compare"], C["teal"]]), legend=alt.Legend(orient="top", title=None)),
            tooltip=["Indicateur", "Version", "Percentile"])
        st.altair_chart(axis_cfg(bars.properties(height=330)), width="stretch")
        st.caption("Gris : première version choisie ; vert d’eau : seconde. Changer les versions dans le menu de gauche.")

# ----------------------------------------------------------------------- entrer en jeu
with tab_sub:
    st.markdown("### Une remplaçante produit plus par minute que la même joueuse titulaire")
    st.markdown(
        "Le par 90 compare des minutes qui ne se valent pas. Pour le vérifier sans mélanger les joueuses ni les "
        "moments du match, on compare **chaque joueuse à elle-même** : ses matchs où elle entre à partir de la 65e "
        "minute, contre ses matchs complets **sur la même fenêtre** (65e minute → fin). 200 joueuses de champ des "
        "quatre championnats, au moins 3 matchs de chaque.")
    sw = load_table("meme_fenetre")
    sw["lab"] = sw.indicateur.map(INDICATORS)
    pooled = sw[sw.perimetre == "4 ligues"].set_index("indicateur")
    cols = st.columns(len(INDICATORS))
    for c, k in zip(cols, INDICATORS):
        r = pooled.loc[k]
        kpi(c, "×" + fr(r.ratio, 2), f"{SHORT[k]}<br>IC 95 % {fr(r.ic95_bas, 2)} à {fr(r.ic95_haut, 2)}")
    k_sel = st.selectbox("Indicateur à détailler par championnat", list(INDICATORS), format_func=INDICATORS.get,
                         index=list(INDICATORS).index("pressures"), key="k_sub")
    d = sw[sw.indicateur == k_sel].copy()
    d["perim"] = d.perimetre.replace({"4 ligues": "4 championnats réunis"})
    order = ["4 championnats réunis"] + LEAGUE_ORDER
    base = alt.Chart(d).encode(y=alt.Y("perim:N", sort=order, title=None))
    rule = base.mark_rule(color=C["compare"], strokeWidth=3).encode(
        x=alt.X("ic95_bas:Q", title="Ratio entrée tardive / titulaire (même fenêtre)",
                scale=alt.Scale(zero=False, nice=False, domain=[min(0.8, d.ic95_bas.min() - 0.05),
                                                                d.ic95_haut.max() + 0.05]),
                axis=alt.Axis(labelExpr=FR_NUM)), x2="ic95_haut:Q")
    dots = base.mark_circle(size=160, stroke=C["bg"], strokeWidth=1.5).encode(
        x="ratio:Q",
        color=alt.condition(alt.datum.perim == "4 championnats réunis", alt.value(C["rust"]), alt.value(C["teal"])),
        tooltip=[alt.Tooltip("perim:N", title="Périmètre"), alt.Tooltip("joueuses:Q", title="Joueuses"),
                 alt.Tooltip("ratio:Q", title="Ratio"), alt.Tooltip("ic95_bas:Q", title="IC bas"),
                 alt.Tooltip("ic95_haut:Q", title="IC haut")])
    one = alt.Chart(pd.DataFrame({"x": [1]})).mark_rule(color=C["ink2"], strokeDash=[4, 4]).encode(x="x:Q")
    st.altair_chart(axis_cfg((rule + dots + one).properties(height=260)), width="stretch")
    st.caption("Point : ratio global ; trait : intervalle de confiance à 95 % (bootstrap sur les joueuses). "
               "À droite de la ligne pointillée, la joueuse produit plus en entrant qu’en jouant tout le match. "
               "Les championnats seuls comptent 26 à 101 joueuses : intervalles plus larges.")
    st.markdown(
        "**Ce que ça change** : le par 90 d’une remplaçante surestime ce qu’elle ferait sur un match entier, "
        "surtout pour le pressing. Pour comparer une remplaçante et une titulaire, regarder la même fenêtre de "
        "match, ou au moins le signaler. **Ce que ça ne dit pas** : pourquoi (fraîcheur, consigne du staff, état "
        "du score) ; la part de possession de l’équipe, elle, est la même dans les deux cas.")

# -------------------------------------------------------------------- méthode et limites
with tab_method:
    st.markdown("""
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
- La normalisation par possession déplace environ **un tiers des joueuses** en pressions et en ballons gagnés, dans les
  quatre championnats, en fonction de la domination de leur équipe ; presque rien en offensif.
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
""")

st.markdown(f"""<div class="jl-foot"><span>Data: StatsBomb (Open Data) · Normalisation par possession inspirée de
SkillCorner</span><span><b style="color:{C['ink']}">Julie Landrevie</b> · Data &amp; performance football
<span class="jl-mono">JL</span></span></div>""", unsafe_allow_html=True)
