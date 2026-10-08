import pytest

from conftest import total_price
from recommender import Recommender

COMPONENTS = {"gpu", "cpu", "motherboard", "ssd", "ram", "psu"}


def test_build_contains_every_component(db):
    build = Recommender(db, 1000, "gaming").recommend()
    assert build is not None
    assert set(build) == COMPONENTS


@pytest.mark.parametrize("budget", [600, 800, 1000, 1500])
def test_build_never_exceeds_budget(db, budget):
    build = Recommender(db, budget, "gaming").recommend()
    if build is not None:
        assert total_price(build) <= budget


def test_cpu_and_motherboard_sockets_match(db):
    build = Recommender(db, 1500, "workstation").recommend()
    assert build["cpu"]["Socket"] == build["motherboard"]["Socket"]


def test_ram_type_matches_motherboard(db):
    for build_type in ("gaming", "workstation"):
        build = Recommender(db, 1500, build_type).recommend()
        assert build["ram"]["RamType"] in build["motherboard"]["RamType"]


def test_gaming_build_picks_best_affordable_gpu(db):
    build = Recommender(db, 1500, "gaming").recommend()
    assert build["gpu"]["Name"] == "GPU Fast"


def test_backtracks_to_cheaper_gpu_when_best_does_not_fit(db):
    # 400 (best GPU) + cheapest rest (180 + 100 + 60 + 40 + 70) = 850 > 700,
    # so the search must back off to the budget GPU.
    build = Recommender(db, 700, "gaming").recommend()
    assert build is not None
    assert build["gpu"]["Name"] == "GPU Budget"
    assert total_price(build) <= 700


def test_workstation_build_prioritises_cpu_score(db):
    build = Recommender(db, 1500, "workstation").recommend()
    assert build["cpu"]["Name"] == "CPU AM5"   # highest WorkStationScore


def test_returns_none_when_budget_too_small(db):
    assert Recommender(db, 100, "gaming").recommend() is None


def test_invalid_build_type_returns_none(db):
    assert Recommender(db, 1000, "office").recommend() is None


def test_build_type_is_case_insensitive(db):
    assert Recommender(db, 1000, "Gaming").recommend() is not None
