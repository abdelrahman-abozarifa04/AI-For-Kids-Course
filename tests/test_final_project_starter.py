"""Tests for projects/final-project-starter (model logic + the Streamlit app end to end)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

STARTER = Path(__file__).resolve().parent.parent / "projects" / "final-project-starter"
sys.path.insert(0, str(STARTER))

from model import load_data, normalize_arabic, predict, train  # noqa: E402


def test_normalize_arabic():
    assert normalize_arabic("جمييييل") == "جميل"
    assert normalize_arabic("أحمد إبراهيم آمنة") == "احمد ابراهيم امنه"


def test_example_data_loads():
    df = load_data()
    assert {"text", "label"} <= set(df.columns)
    assert df["label"].nunique() >= 2
    assert len(df) >= 40


def test_model_learns_better_than_chance():
    result = train(load_data())
    assert result.accuracy > 0.55
    label, probs = predict(result.model, "the food was delicious and the staff were friendly")
    assert label == "positive"
    assert abs(sum(probs.values()) - 1) < 1e-6


def test_bad_csv_is_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"sentence": ["a", "b"], "label": ["x", "y"]}).to_csv(bad, index=False)
    with pytest.raises(ValueError, match="text"):
        load_data(bad)


def test_streamlit_app_runs():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(STARTER / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    at.text_area[0].input("الاكل تحفة والخدمة سريعة")
    at.button[0].click()
    at.run()
    assert not at.exception
    shown = [m.value for m in at.success] + [m.value for m in at.warning]
    assert shown, "the app should show a prediction"
