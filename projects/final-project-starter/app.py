"""Final-project starter: a text-classification web app with Streamlit.

Run:  streamlit run app.py
Swap data/example.csv for your own data (columns: text, label), or upload a CSV in the sidebar.
Code: MIT License.
"""
import io

import pandas as pd
import streamlit as st

from model import DATA_FILE, load_data, predict, train

st.set_page_config(page_title="AI Project Starter", page_icon="🤖", layout="centered")

# ---- Change these to describe YOUR project ----------------------------------
PROJECT_TITLE = "مراجع التعليقات 🍽️"
PROJECT_PITCH = "اكتب تعليق على مطعم بالعامية أو بالإنجليزي، والموديل يقولك إيجابي ولا سلبي."
CONFIDENCE_THRESHOLD = 0.6
# ------------------------------------------------------------------------------

st.title(PROJECT_TITLE)
st.write(PROJECT_PITCH)

with st.sidebar:
    st.header("البيانات")
    uploaded = st.file_uploader("ارفع CSV (أعمدة: text, label)", type="csv")
    source = uploaded if uploaded is not None else DATA_FILE


@st.cache_resource(show_spinner="بندرّب الموديل...")
def get_model(data_key: str, raw: bytes | None):
    df = load_data(io.BytesIO(raw)) if raw else load_data(DATA_FILE)
    return df, train(df)


try:
    raw = uploaded.getvalue() if uploaded is not None else None
    df, result = get_model(uploaded.name if uploaded else "example", raw)
except ValueError as err:
    st.error(f"مشكلة في البيانات: {err}")
    st.stop()

with st.sidebar:
    st.metric("دقة الموديل على بيانات الاختبار", f"{result.accuracy:.0%}")
    st.caption(f"اتدرب على {result.n_train} مثال واتختبر على {result.n_test}.")
    st.bar_chart(df["label"].value_counts())

text = st.text_area("اكتب هنا:", placeholder="الاكل تحفة والخدمة سريعة")
if st.button("حلّل", type="primary") and text.strip():
    label, probs = predict(result.model, text)
    confidence = probs[label]
    if confidence < CONFIDENCE_THRESHOLD:
        st.warning(f"🤔 مش متأكد. أقرب إجابة: **{label}** ({confidence:.0%})")
    else:
        st.success(f"النتيجة: **{label}** ({confidence:.0%})")
    st.bar_chart(pd.Series(probs, name="probability"))

with st.expander("إزاي الموديل ده شغال؟ وحدوده إيه؟"):
    st.markdown(
        "- بيحوّل النص لأرقام (TF-IDF على كلمات وقطع حروف) وبيصنّف بـ Logistic Regression.\n"
        "- اتعلم من بيانات صغيرة، فممكن يغلط في جمل بعيدة عن الأمثلة.\n"
        "- مش بيفهم السخرية، وساعات بيتلخبط في النفي (\"مش وحش\").\n"
        "- **قبل ما تعتمد عليه:** جرّبه مع مستخدمين حقيقيين وقيس."
    )
    st.text(result.report)
