"""Les quatre championnats féminins 2023/24 de StatsBomb Open Data.

Chaque script prend en premier argument une clé de ligue (`wsl`, `fbl`, `ligaf`, `seriea`)
ou `all`. Les données brutes vont dans data_raw/<slug>/, les tables dans
data/processed/*_<slug>.csv, les résultats dans outputs/<slug>/.
"""

LEAGUES = {
    "wsl": {"competition_id": 37, "season_id": 281, "name": "FA WSL", "country": "Angleterre",
            "slug": "wsl_2324"},
    "fbl": {"competition_id": 135, "season_id": 281, "name": "Frauen-Bundesliga", "country": "Allemagne",
            "slug": "fbl_2324"},
    "ligaf": {"competition_id": 182, "season_id": 281, "name": "Liga F", "country": "Espagne",
              "slug": "ligaf_2324"},
    "seriea": {"competition_id": 131, "season_id": 281, "name": "Serie A Women", "country": "Italie",
               "slug": "seriea_2324"},
}


def resolve(arg: str = "wsl") -> list[str]:
    """`all` → les quatre clés ; sinon une clé (ou plusieurs séparées par des virgules)."""
    if arg == "all":
        return list(LEAGUES)
    keys = [a.strip() for a in arg.split(",")]
    unknown = [k for k in keys if k not in LEAGUES]
    if unknown:
        raise SystemExit(f"Ligue inconnue : {', '.join(unknown)}. Choix : {', '.join(LEAGUES)} ou all")
    return keys
