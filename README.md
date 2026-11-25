<div dir="rtl">

# الذكاء الاصطناعي للأطفال والشباب 🤖

[![CI](https://github.com/abdelrahman-abozarifa04/ai-for-kids-course/actions/workflows/ci.yml/badge.svg)](https://github.com/abdelrahman-abozarifa04/ai-for-kids-course/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

**منهج مفتوح ومجاني بالعربي لتعليم الذكاء الاصطناعي من سن ٦ لـ ١٨ سنة.**

🌐 **الموقع:** https://abdelrahman-abozarifa04.github.io/AI-For-Kids-Course/

| | 🧩 المستكشفين الصغار (٦–٩) | 🐍 الشباب (١٥–١٨) |
|---|---|---|
| المدة | ٨ حصص × ٦٠ دقيقة | ٤ تيرمات × ١٢ أسبوع |
| الأجهزة | **ولا حاجة** (unplugged) | لابتوب + Google Colab |
| المحتوى | خطط حصص + ٧٤ كارت للطباعة | ١٦ وحدة + ١٢ notebook بتمارين وحلول |
| المشاريع | "اختراعي الذكي" + حفلة تخرج | شات بوت ← موديل صور ← مساعد ← تطبيق ويب |
| ابدأ من | [`docs/kids`](docs/kids/index.md) | [`docs/teens`](docs/teens/index.md) |

## ليه؟

- **بالعربي وبأمثلة من حياتنا:** كشري، أسعار شقق بالجنيه، تعليقات بالعامية المصرية.
- **من غير أجهزة للصغيرين:** ينفع في أي فصل.
- **كل الكود مجرّب:** الـ CI بيشغّل كل notebook وكل حل تمرين مع كل تعديل.
- **مفتوح:** انسخ، اطبع، ترجم، ودرّس، حتى في كورسات بفلوس.

</div>

## Quick start

```bash
pip install -r requirements-dev.txt
pytest                              # executes all notebooks + solutions, card and app tests
python tools/build_cards.py --pdf   # printable card sheets -> docs/printables/
mkdocs serve                        # preview the website
```

Or open any notebook directly in Colab from the [teens track page](docs/teens/index.md).

## Repository layout

```text
docs/kids/                  8 unplugged lesson plans + teacher guide (Arabic)
docs/teens/                 4 terms, 16 units, teacher guide (Arabic)
docs/printables/            generated card sheets (HTML + PDF)
cards/cards.yaml            source of all 74 kids' cards (7 decks)
tools/build_cards.py        card sheet generator
notebooks/teens/term-*/     12 Colab-ready notebooks
projects/final-project-starter/   Streamlit app template for the final project
tests/                      notebook, solution, card and app tests
```

## English

An open, Arabic-first AI curriculum for ages 6–18: an unplugged track for ages 6–9 with printable cards, and a four-term Python/ML track for ages 15–18 with tested Colab notebooks (including Egyptian-Arabic NLP). See the [English overview](docs/en.md).

## Roadmap

Classroom pilots, a full English edition, a 10–14 middle track, and a card editor. See [ROADMAP.md](ROADMAP.md).

## Contributing

Teachers' classroom reports, translations, new card decks, and notebooks are all welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Code © Abdelrahman Sami and contributors, [MIT](LICENSE). Educational content [CC BY 4.0](LICENSE-CONTENT.md).
