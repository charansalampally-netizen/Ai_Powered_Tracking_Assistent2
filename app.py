import streamlit as st
import pandas as pd

from utils import *
from prompts import *

st.set_page_config(
    page_title="Asset-Tracking Assistant",
    layout="wide"
)

st.title("💻 Asset-Tracking Assistant")

st.write(WELCOME_MESSAGE)

try:

    df = load_assets()

    st.success("Asset data loaded successfully!")

    st.write(f"Total Assets: {len(df)}")

except Exception as e:

    st.error("Error loading CSV")

    st.exception(e)

    st.stop()


question = st.text_input(
    "Ask a question about your assets"
)

if st.button("Submit"):

    if question == "":

        st.warning("Please enter a question.")

    else:

        results = search_assets(df, question)

        st.subheader("Results")

        if results.empty:

            st.write("No matching assets found.")

        else:

            st.dataframe(results)