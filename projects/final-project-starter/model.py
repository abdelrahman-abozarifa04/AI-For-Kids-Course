"""Model logic for the final-project starter, kept separate from the UI so it can be tested.

Replace the example data in data/example.csv with your own: two columns, `text` and `label`.
Code: MIT License.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline, make_union

DATA_FILE = Path(__file__).parent / "data" / "example.csv"


def normalize_arabic(text: str) -> str:
    """Unify common Arabic letter variants and remove stretched letters, so Egyptian Arabic matches better."""
    text = str(text).lower()
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"[ً-ْ]", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    return text


def load_data(path: Path | str = DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = {"text", "label"} - set(df.columns)
    if missing:
        raise ValueError(f"CSV must have columns 'text' and 'label'; missing: {sorted(missing)}")
    df = df.dropna(subset=["text", "label"]).drop_duplicates(subset=["text"])
    if df["label"].nunique() < 2:
        raise ValueError("Need at least two different labels to train a classifier")
    return df.reset_index(drop=True)


def build_model() -> Pipeline:
    features = make_union(
        TfidfVectorizer(preprocessor=normalize_arabic),
        TfidfVectorizer(preprocessor=normalize_arabic, analyzer="char_wb", ngram_range=(2, 4)),
    )
    return make_pipeline(features, LogisticRegression(max_iter=1000, C=10))


@dataclass
class TrainResult:
    model: Pipeline
    accuracy: float
    report: str
    n_train: int
    n_test: int


def train(df: pd.DataFrame, test_size: float = 0.25, seed: int = 0) -> TrainResult:
    stratify = df["label"] if df["label"].value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=test_size, random_state=seed, stratify=stratify)
    model = build_model().fit(X_train, y_train)
    pred = model.predict(X_test)
    result = TrainResult(model, accuracy_score(y_test, pred),
                         classification_report(y_test, pred, zero_division=0), len(X_train), len(X_test))
    # Final model learns from all the data once we have measured it honestly on the test split.
    result.model = build_model().fit(df["text"], df["label"])
    return result


def predict(model: Pipeline, text: str) -> tuple[str, dict[str, float]]:
    probs = model.predict_proba([text])[0]
    ranked = dict(sorted(zip(model.classes_, probs), key=lambda kv: -kv[1]))
    return next(iter(ranked)), {str(k): float(v) for k, v in ranked.items()}
