"""Téléchargement StatsBomb Open Data — championnats féminins 2023/24 (voir src/leagues.py).

Données : StatsBomb Open Data (https://github.com/statsbomb/open-data).
Crédit obligatoire sur tout visuel public : « Data: StatsBomb ».

Usage : python src/download.py <wsl|fbl|ligaf|seriea|all> [dossier_raw]
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from leagues import LEAGUES, resolve

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"


def fetch(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as r:
        dest.write_bytes(r.read())


def download_league(key: str, raw_root: str = "data_raw") -> None:
    lg = LEAGUES[key]
    comp, season = lg["competition_id"], lg["season_id"]
    raw = Path(raw_root) / lg["slug"]
    matches_file = raw / f"matches_{comp}_{season}.json"
    fetch(f"{BASE}/matches/{comp}/{season}.json", matches_file)
    ids = [m["match_id"] for m in json.loads(matches_file.read_text())]

    jobs = []
    for mid in ids:
        jobs.append((f"{BASE}/events/{mid}.json", raw / "events" / f"{mid}.json"))
        jobs.append((f"{BASE}/lineups/{mid}.json", raw / "lineups" / f"{mid}.json"))
    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(lambda j: fetch(*j), jobs))
    print(f"{lg['name']} : {len(ids)} matchs, événements et compositions dans {raw}/")


def main(league: str = "wsl", raw_root: str = "data_raw") -> None:
    for key in resolve(league):
        download_league(key, raw_root)


if __name__ == "__main__":
    main(*sys.argv[1:])
