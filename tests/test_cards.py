"""Validate cards.yaml, the sheet generator, and that lesson plans reference real decks."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_cards  # noqa: E402

KIDS_DOCS = ROOT / "docs" / "kids"


def test_cards_yaml_is_valid():
    decks = build_cards.load_decks()
    assert len(decks) >= 7
    assert sum(len(d["cards"]) for d in decks) >= 70


def test_every_session_has_a_lesson_plan():
    for deck in build_cards.load_decks():
        plan = KIDS_DOCS / f"session-{int(deck['session']):02d}.md"
        assert plan.exists(), f"deck {deck['id']} points to missing {plan.name}"
        assert f"`{deck['id']}`" in plan.read_text(encoding="utf-8"), \
            f"{plan.name} should mention its deck `{deck['id']}`"


def test_lesson_plans_only_reference_existing_card_ids():
    ids = {c["id"] for d in build_cards.load_decks() for c in d["cards"]}
    for plan in KIDS_DOCS.glob("session-*.md"):
        for ref in re.findall(r"`([a-z]{3}-\d{2})`", plan.read_text(encoding="utf-8")):
            assert ref in ids, f"{plan.name} references unknown card {ref}"


def test_zozo_rule_is_consistent():
    """Session 5's secret rule: a Zozo has exactly three eyes."""
    zozo = next(d for d in build_cards.load_decks() if d["id"] == "zozo")
    for card in zozo["cards"]:
        eyes = card["emoji"].count("👁")
        assert card["tags"]["zozo"] == (eyes == 3), card["id"]
    assert sum(1 for c in zozo["cards"] if c["tags"].get("test")) == 2


def test_animal_decision_tree_leaves_match_tags():
    """Session 7 draws a tree: fur -> pet / water -> flies. Every animal must land in exactly one leaf."""
    animals = next(d for d in build_cards.load_decks() if d["id"] == "animals")["cards"]
    leaves = {}
    for a in animals:
        t = a["tags"]
        key = ("fur", t["pet"]) if t["fur"] else ("water",) if t["water"] else ("flies", t["flies"])
        leaves.setdefault(key, []).append(a["emoji"])
    assert ("flies", False) not in leaves, "a non-furry land animal that doesn't fly breaks the tree"


def test_build_writes_html(tmp_path):
    written = build_cards.build(tmp_path)
    names = {p.name for p in written}
    assert "index.html" in names
    for deck in build_cards.load_decks():
        html = (tmp_path / f"{deck['id']}.html").read_text(encoding="utf-8")
        assert html.startswith("<!DOCTYPE html>")
        assert html.count('class="card"') == len(deck["cards"])


def test_duplicate_ids_are_rejected(tmp_path):
    bad = {"decks": [{"id": "d", "title_ar": "x", "title_en": "x", "color": "#000000", "session": 1,
                      "cards": [{"id": "a", "emoji": "x", "ar": "x", "en": "x"},
                                {"id": "a", "emoji": "y", "ar": "y", "en": "y"}]}]}
    path = tmp_path / "cards.yaml"
    path.write_text(yaml.safe_dump(bad, allow_unicode=True), encoding="utf-8")
    with pytest.raises(build_cards.CardError, match="duplicate"):
        build_cards.load_decks(path)
