import streamlit as st

from utils import (
    active_assets,
    assets_due_for_maintenance,
    assets_not_seen_recently,
    load_assets,
    query_assets,
)

st.set_page_config(
    page_title="Asset Tracking Assistant",
    page_icon="💼",
    layout="wide",
)

st.title("💻 Asset Tracking Assistant")
st.markdown(
    """
    Welcome to the Asset Tracking Assistant.

    Ask natural language questions about your company assets.

    Examples:
    - Where is asset A001?
    - Which assets have not been seen in 30 days?
    - Show maintenance due assets.
    - List inactive assets.
    - Show assets in Finance.
    """
)

try:
    df = load_assets()
except Exception as exc:
    st.error(f"Error loading asset data: {exc}")
    st.stop()

total_assets = len(df)
active_count = len(active_assets(df))
maintenance_count = len(assets_due_for_maintenance(df))
not_seen_count = len(assets_not_seen_recently(df))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total assets", total_assets)
col2.metric("Active assets", active_count)
col3.metric("Maintenance due", maintenance_count)
col4.metric("Not seen in 30 days", not_seen_count)

st.markdown("---")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("question_form"):
    question = st.text_input(
        "Ask a question about company assets",
        placeholder="Where is Laptop A001?",
        key="question_input",
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    if not question:
        st.warning("Please enter a question before submitting.")
    else:
        answer = query_assets(df, question)
        st.session_state.history.append({
            "question": question,
            "answer": answer,
        })

if st.session_state.history:
    st.markdown("### Chat history")
    for entry in st.session_state.history:
        st.markdown(f"**You:** {entry['question']}")
        if isinstance(entry["answer"], str):
            st.markdown(f"**Assistant:** {entry['answer']}")
        else:
            st.markdown(f"**Assistant:** Found {len(entry['answer'])} matching asset(s)")
            st.dataframe(entry["answer"], use_container_width=True)
else:
    st.info("Ask a question to see answers about assets.")
