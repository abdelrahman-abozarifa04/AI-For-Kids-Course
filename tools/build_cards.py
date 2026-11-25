#!/usr/bin/env python3
"""Build printable card sheets for the Kids track.

Reads cards/cards.yaml and writes one print-ready A4 HTML file per deck,
plus an index page, into an output folder (default: docs/printables).
Optionally renders each sheet to PDF with a headless Chrome/Chromium.

Usage:
    python tools/build_cards.py                 # HTML only
    python tools/build_cards.py --pdf           # HTML + PDF (needs Chrome/Chromium)
    python tools/build_cards.py --out build/    # custom output folder
    python tools/build_cards.py --check         # validate the YAML only

Code: MIT License. Card content: CC BY 4.0 (see LICENSE-CONTENT.md).
"""
from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CARDS_FILE = ROOT / "cards" / "cards.yaml"
DEFAULT_OUT = ROOT / "docs" / "printables"

REQUIRED_DECK_FIELDS = ("id", "title_ar", "title_en", "color", "session", "cards")
REQUIRED_CARD_FIELDS = ("id", "emoji", "ar", "en")
CARDS_PER_PAGE = 9

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
@page { size: A4; margin: 10mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Cairo', 'DejaVu Sans', 'Noto Color Emoji', sans-serif; color: #1f2937; }
.sheet { page-break-after: always; break-after: page; }
.sheet:last-child { page-break-after: auto; break-after: auto; }
.sheet-header { display: flex; justify-content: space-between; align-items: baseline;
  font-size: 10pt; color: #6b7280; margin-bottom: 4mm; }
.grid { display: grid; grid-template-columns: repeat(3, 63mm); grid-auto-rows: 86mm;
  gap: 0; justify-content: center; }
.card { position: relative; border: 0.4mm dashed #9ca3af; padding: 4mm; display: flex;
  flex-direction: column; align-items: center; justify-content: space-between; overflow: hidden; }
.card .band { position: absolute; inset: 0 0 auto 0; height: 9mm; background: var(--deck);
  color: #fff; font-size: 8.5pt; font-weight: 700; display: flex; align-items: center;
  justify-content: center; }
.card .emoji { margin-top: 10mm; font-size: 30pt; line-height: 1.15; text-align: center;
  font-family: 'Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif; word-break: break-all; }
.card .emoji.long { font-size: 19pt; }
.card .ar { font-size: 14pt; font-weight: 700; text-align: center; direction: rtl; line-height: 1.35; }
.card .ar.small { font-size: 11pt; }
.card .en { font-size: 8.5pt; color: #6b7280; text-align: center; direction: ltr; }
.card .hint { font-size: 8pt; color: #374151; text-align: center; direction: rtl;
  background: #f3f4f6; border-radius: 2mm; padding: 1mm 2mm; }
.card .answer { font-size: 8pt; color: #6b7280; direction: rtl; text-align: center;
  transform: rotate(180deg); border-top: 0.3mm dotted #d1d5db; width: 100%; padding-top: 1mm; }
.card .tag { position: absolute; top: 10.5mm; left: 2mm; font-size: 7pt; font-weight: 700;
  color: var(--deck); border: 0.3mm solid var(--deck); border-radius: 1mm; padding: 0 1mm; }
.card .id { position: absolute; bottom: 1mm; left: 2mm; font-size: 6pt; color: #9ca3af; direction: ltr; }
.footer { text-align: center; font-size: 7pt; color: #9ca3af; margin-top: 3mm; }
@media screen { body { background: #e5e7eb; } .sheet { background: #fff; width: 210mm;
  margin: 8mm auto; padding: 10mm; box-shadow: 0 1mm 4mm rgba(0,0,0,.15); } }
"""


class CardError(ValueError):
    """Raised when cards.yaml is malformed."""


def load_decks(path: Path = CARDS_FILE) -> list[dict]:
    """Load and validate all decks. Raises CardError on the first problem found."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "decks" not in data:
        raise CardError(f"{path}: top-level 'decks' list is missing")

    decks = data["decks"]
    seen_decks: set[str] = set()
    seen_cards: set[str] = set()
    for deck in decks:
        for field in REQUIRED_DECK_FIELDS:
            if field not in deck:
                raise CardError(f"deck {deck.get('id', '?')}: missing field '{field}'")
        if deck["id"] in seen_decks:
            raise CardError(f"duplicate deck id '{deck['id']}'")
        seen_decks.add(deck["id"])
        if not str(deck["color"]).startswith("#"):
            raise CardError(f"deck {deck['id']}: color must be a hex value like #4F46E5")
        if not deck["cards"]:
            raise CardError(f"deck {deck['id']}: has no cards")
        for card in deck["cards"]:
            for field in REQUIRED_CARD_FIELDS:
                if not card.get(field):
                    raise CardError(f"card {card.get('id', '?')} in {deck['id']}: missing '{field}'")
            if card["id"] in seen_cards:
                raise CardError(f"duplicate card id '{card['id']}'")
            seen_cards.add(card["id"])
    return decks


def _e(text: object) -> str:
    return html.escape(str(text), quote=True)


def render_card(card: dict, deck: dict, show_answers: bool) -> str:
    emoji = str(card["emoji"])
    emoji_class = "emoji long" if len(emoji) > 4 else "emoji"
    ar_class = "ar small" if len(str(card["ar"])) > 22 else "ar"
    parts = [
        f'<div class="card" style="--deck:{_e(deck["color"])}">',
        f'<div class="band">{_e(deck["title_ar"])}</div>',
    ]
    if card.get("tags", {}).get("test"):
        parts.append('<div class="tag">اختبار</div>')
    parts.append(f'<div class="{emoji_class}">{_e(emoji)}</div>')
    parts.append(f'<div class="{ar_class}">{_e(card["ar"])}</div>')
    parts.append(f'<div class="en">{_e(card["en"])}</div>')
    if card.get("hint_ar"):
        parts.append(f'<div class="hint">{_e(card["hint_ar"])}</div>')
    if show_answers and card.get("answer_ar"):
        parts.append(f'<div class="answer">{_e(card["answer_ar"])}</div>')
    parts.append(f'<div class="id">{_e(card["id"])}</div>')
    parts.append("</div>")
    return "".join(parts)


def render_deck(deck: dict, show_answers: bool = True) -> str:
    cards = deck["cards"]
    pages = [cards[i:i + CARDS_PER_PAGE] for i in range(0, len(cards), CARDS_PER_PAGE)]
    sheets = []
    for n, page in enumerate(pages, start=1):
        cells = "".join(render_card(c, deck, show_answers) for c in page)
        sheets.append(
            '<section class="sheet">'
            f'<div class="sheet-header"><span>{_e(deck["title_en"])} — Session {_e(deck["session"])}</span>'
            f'<span dir="rtl">{_e(deck["title_ar"])} — صفحة {n} من {len(pages)}</span></div>'
            f'<div class="grid">{cells}</div>'
            '<div class="footer">AI-For-Kids-Course · CC BY 4.0 · github.com/abdelrahman-abozarifa04/ai-for-kids-course</div>'
            "</section>"
        )
    return (
        '<!DOCTYPE html><html lang="ar"><head><meta charset="utf-8">'
        f'<title>{_e(deck["title_en"])} — printable cards</title>'
        f"<style>{CSS}</style></head><body>{''.join(sheets)}</body></html>"
    )


def render_index(decks: list[dict]) -> str:
    rows = "".join(
        f'<li><a href="{_e(d["id"])}.html">{_e(d["title_ar"])} — {_e(d["title_en"])}</a> '
        f'(الحصة {_e(d["session"])}، {len(d["cards"])} كارت)</li>'
        for d in decks
    )
    return (
        '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
        "<title>Printable cards</title>"
        "<style>body{font-family:'Cairo','DejaVu Sans',sans-serif;max-width:720px;margin:2rem auto;line-height:1.9}</style>"
        f"</head><body><h1>كروت للطباعة</h1><p>اطبع على A4 وقص على الخط المتقطع.</p><ul>{rows}</ul></body></html>"
    )


def find_chrome() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    return None


def html_to_pdf(chrome: str, src: Path, dst: Path) -> None:
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
         f"--print-to-pdf={dst}", src.resolve().as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
    )


def build(out: Path, pdf: bool = False, show_answers: bool = True) -> list[Path]:
    decks = load_decks()
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for deck in decks:
        target = out / f"{deck['id']}.html"
        target.write_text(render_deck(deck, show_answers), encoding="utf-8")
        written.append(target)
    index = out / "index.html"
    index.write_text(render_index(decks), encoding="utf-8")
    written.append(index)

    if pdf:
        chrome = find_chrome()
        if not chrome:
            raise SystemExit("--pdf needs Chrome or Chromium on PATH")
        for deck in decks:
            src = out / f"{deck['id']}.html"
            dst = out / f"{deck['id']}.pdf"
            html_to_pdf(chrome, src, dst)
            written.append(dst)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output folder")
    parser.add_argument("--pdf", action="store_true", help="also render PDFs with headless Chrome")
    parser.add_argument("--no-answers", action="store_true", help="hide the upside-down answer strip")
    parser.add_argument("--check", action="store_true", help="only validate cards.yaml")
    args = parser.parse_args(argv)

    try:
        decks = load_decks()
    except CardError as err:
        print(f"cards.yaml error: {err}", file=sys.stderr)
        return 1
    if args.check:
        total = sum(len(d["cards"]) for d in decks)
        print(f"OK: {len(decks)} decks, {total} cards")
        return 0

    for path in build(args.out, pdf=args.pdf, show_answers=not args.no_answers):
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
