"""Téléchargement StatsBomb Open Data — FA WSL 2023/24 (competition 37, saison 281).

Données : StatsBomb Open Data (https://github.com/statsbomb/open-data).
Crédit obligatoire sur tout visuel public : « Data: StatsBomb ».

Usage : python src/download.py [dossier_raw]
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMP, SEASON = 37, 281


def fetch(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as r:
        dest.write_bytes(r.read())


def main(raw_dir: str = "data_raw") -> None:
    raw = Path(raw_dir)
    matches_file = raw / f"matches_{COMP}_{SEASON}.json"
    fetch(f"{BASE}/matches/{COMP}/{SEASON}.json", matches_file)
    ids = [m["match_id"] for m in json.loads(matches_file.read_text())]

    jobs = []
    for mid in ids:
        jobs.append((f"{BASE}/events/{mid}.json", raw / "events" / f"{mid}.json"))
        jobs.append((f"{BASE}/lineups/{mid}.json", raw / "lineups" / f"{mid}.json"))
    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(lambda j: fetch(*j), jobs))
    print(f"{len(ids)} matchs : événements et compositions dans {raw}/")


if __name__ == "__main__":
    main(*sys.argv[1:])
