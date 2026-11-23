"""Tests des fonctions de calcul (sans téléchargement : données synthétiques)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analyze_rankings import pct_in_position, spearman  # noqa: E402
from build_indicators import is_progressive, match_counts, opponent_factors  # noqa: E402
from build_player_match import clock_to_s, overlap, process_match, ts_to_s  # noqa: E402

HOME, AWAY = 1, 2


def ev(i, typ, period, ts, team, poss, poss_team, player=None, minute=0, **extra):
    e = {"id": f"e{i}", "type": {"name": typ}, "period": period, "timestamp": ts, "minute": minute,
         "team": {"id": team}, "possession": poss, "possession_team": {"id": poss_team}, "duration": 0.0}
    if player is not None:
        e["player"] = {"id": player}
    e.update(extra)
    return e


def lineup(team_id, players):
    return {"team_id": team_id, "team_name": f"T{team_id}",
            "lineup": [{"player_id": p, "player_name": f"P{p}", "player_nickname": None,
                        "positions": [{"position": "Center Back", "start_reason": "Starting XI"}]}
                       for p in players]}


@pytest.fixture
def mini_match():
    """Match de 2 × 45 min : la joueuse 11 est remplacée par la 12 à la 60e, la 21 expulsée à la 80e."""
    home_xi = [{"player": {"id": p}} for p in [11, 13]]
    away_xi = [{"player": {"id": p}} for p in [21, 22]]
    events = [
        ev(0, "Starting XI", 1, "00:00:00.000", HOME, 1, HOME, tactics={"lineup": home_xi}),
        ev(1, "Starting XI", 1, "00:00:00.000", AWAY, 1, HOME, tactics={"lineup": away_xi}),
        ev(2, "Pass", 1, "00:00:00.000", HOME, 1, HOME, player=11, duration=600.0),   # possession 1 : 10 min
        ev(3, "Pass", 1, "00:20:00.000", AWAY, 2, AWAY, player=21, duration=600.0),   # possession 2 : 10 min
        ev(4, "Half End", 1, "00:45:00.000", HOME, 2, AWAY),
        ev(5, "Substitution", 2, "00:15:00.000", HOME, 3, HOME, player=11,
           substitution={"replacement": {"id": 12}}),
        ev(6, "Pass", 2, "00:20:00.000", HOME, 3, HOME, player=12, duration=300.0),   # possession 3 : 5 min
        ev(7, "Foul Committed", 2, "00:35:00.000", AWAY, 3, HOME, player=21,
           foul_committed={"card": {"name": "Red Card"}}),
        ev(8, "Half End", 2, "00:45:00.000", HOME, 3, HOME),
    ]
    match = {"match_id": 99, "match_date": "2024-01-01", "match_week": 1,
             "home_team": {"home_team_id": HOME, "home_team_name": "T1"},
             "away_team": {"away_team_id": AWAY, "away_team_name": "T2"},
             "home_score": 0, "away_score": 0}
    rows = process_match(match, events, [lineup(HOME, [11, 12, 13]), lineup(AWAY, [21, 22])])
    return {r["player_id"]: r for r in rows}


def test_clock_conversions():
    assert clock_to_s("45:30") == 2730
    assert ts_to_s("01:02:03.500") == pytest.approx(3723.5)
    assert overlap(0, 10, 5, 20) == 5
    assert overlap(0, 10, 20, 30) == 0


def test_minutes_from_events(mini_match):
    assert mini_match[11]["minutes_played"] == pytest.approx(60)   # remplacée à la 60e
    assert mini_match[12]["minutes_played"] == pytest.approx(30)   # entrée à la 60e
    assert mini_match[13]["minutes_played"] == pytest.approx(90)
    assert mini_match[21]["minutes_played"] == pytest.approx(80)   # expulsée à la 80e
    assert mini_match[11]["starter"] and not mini_match[12]["starter"]


def test_possession_during_presence(mini_match):
    # la 11 voit les possessions 1 (10 min, son équipe) et 2 (10 min, adverse), pas la 3
    assert mini_match[11]["team_possession_s_on"] == pytest.approx(600)
    assert mini_match[11]["opp_possession_s_on"] == pytest.approx(600)
    # la 12 (entrée à la 60e) ne voit que la possession 3 : de la passe (65e) à la faute
    # (80e) = 15 min ; la fin de match et le remplacement (événements administratifs)
    # ne la prolongent pas
    assert mini_match[12]["team_possession_s_on"] == pytest.approx(900)
    assert mini_match[12]["opp_possession_s_on"] == 0


def test_admin_events_do_not_extend_possession(mini_match):
    # possession 2 : passe à la 20e (10 min) puis « Half End » à la 45e, qui ne compte pas
    assert mini_match[13]["opp_possession_s_on"] == pytest.approx(600)


def test_is_progressive():
    assert is_progressive([60, 40], [90, 40])          # 60 m → 30 m du but
    assert not is_progressive([30, 40], [90, 40])      # départ dans ses 40 %
    assert not is_progressive([60, 40], [70, 40])      # 60 m → 50 m : moins de 25 %


def test_match_counts_rules():
    events = [
        {"id": "s1", "type": {"name": "Shot"}, "period": 1, "player": {"id": 9},
         "shot": {"type": {"name": "Open Play"}, "statsbomb_xg": 0.3}},
        {"id": "s2", "type": {"name": "Shot"}, "period": 1, "player": {"id": 9},
         "shot": {"type": {"name": "Penalty"}, "statsbomb_xg": 0.78}},
        {"id": "p1", "type": {"name": "Pass"}, "period": 1, "player": {"id": 8}, "location": [60, 40],
         "pass": {"assisted_shot_id": "s1", "end_location": [100, 40]}},
        {"id": "p2", "type": {"name": "Pass"}, "period": 1, "player": {"id": 8}, "location": [60, 40],
         "pass": {"type": {"name": "Free Kick"}, "end_location": [100, 40]}},
        {"id": "r1", "type": {"name": "Ball Recovery"}, "period": 1, "player": {"id": 7},
         "ball_recovery": {"recovery_failure": True}},
        {"id": "r2", "type": {"name": "Ball Recovery"}, "period": 1, "player": {"id": 7}},
        {"id": "i1", "type": {"name": "Interception"}, "period": 1, "player": {"id": 7},
         "interception": {"outcome": {"name": "Lost Out"}}},
    ]
    c = match_counts(events)
    assert c[9]["npxg"] == pytest.approx(0.3)           # penalty exclu
    assert c[8]["xa"] == pytest.approx(0.3)             # xA = xG du tir qui suit la passe
    assert c[8]["prog"] == 1                            # coup franc exclu
    assert c[7]["ball_wins"] == 1                       # récupération ratée et interception perdue exclues


def test_opponent_factor_excludes_own_team():
    # A, B, C. Contre C, l'équipe A produit 10, l'équipe B produit 2 : pour A, le facteur de C
    # ne doit dépendre que de B.
    rows = []
    for mid, (t, o, v) in enumerate([(1, 3, 10), (2, 3, 2), (1, 2, 4), (2, 1, 4), (3, 1, 4), (3, 2, 4)]):
        rows.append({"match_id": mid, "team_id": t, "opponent_id": o, "minutes_played": 990.0,
                     "npxg": v, "xa": v, "prog": v, "pressures": v, "ball_wins": v})
    f = opponent_factors(pd.DataFrame(rows)).set_index(["team_id", "opponent_id"])
    league = 28 / 6
    assert f.loc[(1, 3), "f_npxg"] == pytest.approx(2 / league)
    assert f.loc[(2, 3), "f_npxg"] == pytest.approx(10 / league)


def test_percentile_within_position():
    df = pd.DataFrame({"position_group": ["CB", "CB", "FW", "FW"], "x": [1, 2, 10, 20]})
    assert list(pct_in_position(df, "x")) == [0.5, 1.0, 0.5, 1.0]


def test_spearman():
    assert spearman(pd.Series([1, 2, 3]), pd.Series([10, 20, 30])) == pytest.approx(1.0)
    assert spearman(pd.Series([1, 2, 3]), pd.Series([3, 2, 1])) == pytest.approx(-1.0)


# ------------------------------------------------------------------ étape 4 : ligues, application
def test_resolve_leagues():
    from leagues import resolve
    assert resolve("all") == ["wsl", "fbl", "ligaf", "seriea"]
    assert resolve("wsl,seriea") == ["wsl", "seriea"]
    with pytest.raises(SystemExit):
        resolve("d1arkema")


def test_first_phase_is_one_round_robin():
    from analyze_rankings import first_phase
    # 4 équipes → 1re phase = journées 1 à 3 (chaque adversaire une fois)
    pm = pd.DataFrame({"team_id": [1, 2, 3, 4] * 6, "match_week": sorted(list(range(1, 7)) * 4)})
    fp = first_phase(pm)
    assert set(pm[fp].match_week) == {1, 2, 3}
    assert set(pm[~fp].match_week) == {4, 5, 6}


def test_app_runs_without_error():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest
    root = Path(__file__).resolve().parents[1]
    if not (root / "data/processed/player_season_versions_all_2324.csv").exists():
        pytest.skip("table commune absente : lancer src/compare_leagues.py")
    at = AppTest.from_file(str(root / "streamlit_app.py"), default_timeout=60).run()
    assert not at.exception
    at.sidebar.selectbox[0].set_value("Serie A Women").run()
    at.sidebar.selectbox[1].set_value("FW").run()
    at.sidebar.selectbox[3].set_value("total").run()
    at.sidebar.radio[0].set_value("eligible_900").run()
    assert not at.exception
