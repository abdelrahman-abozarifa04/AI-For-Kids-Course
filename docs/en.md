# English overview

<div dir="ltr" markdown>

**AI-For-Kids-Course** is an open, Arabic-first curriculum for teaching artificial intelligence to learners aged 6 to 18. Lesson plans are written in Arabic (with Egyptian-dialect classroom scripts); code, notebooks' code cells, and technical terms are in English.

## Tracks

### Little Explorers (ages 6–9): unplugged

Eight 60-minute sessions that need **no computers, tablets, or internet**, designed for classrooms without devices. Children discover core ideas through card games and movement:

| # | Session | Concept |
|---|---|---|
| 1 | AI or Not? | What makes something "AI" |
| 2 | The Obedient Robot | Algorithms, debugging |
| 3 | Pattern Hunter | Patterns and prediction |
| 4 | Sorting Supermarket | Classification by features |
| 5 | Who is a Zozo? | Learning from examples, train vs. test |
| 6 | The Robot that Learned Wrong | Data and bias |
| 7 | The Question Game | Decision trees |
| 8 | AI and Us + Graduation | Safe, honest, fair use |

74 printable cards across 7 decks are generated from `cards/cards.yaml` by `tools/build_cards.py` (HTML, and PDF via headless Chrome).

### Teens (ages 15–18): Python and machine learning

A two-year, four-term program. 12 Jupyter notebooks that run in Google Colab in seconds, with no GPU and no downloads:

- **Term 1:** Python basics, data cleaning and visualization, AI ethics. *Project: rule-based chatbot.*
- **Term 2:** Supervised/unsupervised learning, regression, decision trees, overfitting, neural networks from scratch. *Project: shape recognizer with robustness testing.*
- **Term 3:** NLP with English **and Egyptian Arabic** sentiment analysis, computer vision and hand-written convolution, BFS and Q-learning robots, generative models. *Project: intent-classifying assistant.*
- **Term 4:** AI in business, AI for good, project planning with GitHub, Streamlit deployment. *Project: a real AI web app (starter kit included).*

Every exercise has a hidden solution, and **CI executes every notebook and every solution** on each change.

## Run it locally

```bash
git clone https://github.com/abdelrahman-abozarifa04/ai-for-kids-course
cd ai-for-kids-course
pip install -r requirements-dev.txt
pytest                                # run notebooks, solutions, card and app tests
python tools/build_cards.py --pdf     # build printable cards
mkdocs serve                          # preview this website
```

## License

Code: [MIT](https://github.com/abdelrahman-abozarifa04/ai-for-kids-course/blob/main/LICENSE). Educational content: [CC BY 4.0](https://github.com/abdelrahman-abozarifa04/ai-for-kids-course/blob/main/LICENSE-CONTENT.md). Use it, print it, translate it, and teach with it, including in paid courses.

## Contributing

Translations (especially a full English edition), classroom feedback, new card decks, and new notebooks are welcome. See [CONTRIBUTING.md](https://github.com/abdelrahman-abozarifa04/ai-for-kids-course/blob/main/CONTRIBUTING.md).

</div>
