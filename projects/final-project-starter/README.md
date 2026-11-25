# Final Project Starter · عدة المشروع النهائي

تطبيق ويب جاهز بـ **Streamlit** بيدرّب موديل تصنيف نصوص ويعرضه. ابدأ منه، وغيّر البيانات والفكرة لمشروعك.

## شغّله في ٣ خطوات

```bash
pip install -r requirements.txt
streamlit run app.py
```

المتصفح هيفتح على `http://localhost:8501`.

## غيّره لمشروعك

| عايز تغيّر | فين |
|---|---|
| البيانات | `data/example.csv` (عمودين: `text` و `label`)، أو ارفع CSV من التطبيق |
| العنوان والوصف | أول سطور في `app.py` (`PROJECT_TITLE`, `PROJECT_PITCH`) |
| الموديل | `build_model()` في `model.py` |
| حد الثقة | `CONFIDENCE_THRESHOLD` في `app.py` |

**مشروعك مش نصوص؟** (صور، أرقام) نفس الهيكل بالظبط: `model.py` فيه `load_data` و `train` و `predict`، و`app.py` بيعرضهم. غيّر الموديل والمدخلات بس.

## الملفات

```text
final-project-starter/
├── app.py                 # الواجهة (Streamlit)
├── model.py               # البيانات والتدريب والتوقع (من غير واجهة، علشان يتختبر)
├── data/example.csv       # ٦٠ تعليق: إنجليزي + عامية مصرية
├── requirements.txt
└── PROPOSAL_TEMPLATE.md   # نموذج مقترح المشروع
```

## انشره مجاناً
1. ارفع المشروع على GitHub.
2. ادخل [share.streamlit.io](https://share.streamlit.io) واختار الـ repo والملف `app.py`.

## الاختبارات
من جذر المشروع: `pytest tests/test_final_project_starter.py`

---

A ready-to-run Streamlit text-classification app (English + Egyptian Arabic example data). Replace `data/example.csv` with your own `text,label` data. MIT licensed.
