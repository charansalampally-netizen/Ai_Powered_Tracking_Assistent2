import streamlit as st
import pandas as pd

st.write("The app started successfully!")

from utils import (
    load_assets,
    process_question,
    active_assets,
    assets_due_for_maintenance
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Asset Tracking Assistant",
    page_icon="💻",
    layout="wide"
)

# --------------------------------------------------
# Load Asset Data
# --------------------------------------------------

try:
    df = load_assets()

except Exception as e:
    st.error(f"Error loading asset data:\n\n{e}")
    st.stop()

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("💻 Asset Tracking Assistant")

st.write("""
Welcome to the Asset Tracking Assistant!

Ask questions such as:

- Where is asset A001?
- Where is the Dell Laptop?
- Show maintenance due assets.
- Show all active assets.
- Show assets in Finance.
- Which assets have not been seen recently?
""")

# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------

total_assets = len(df)

active_count = len(active_assets(df))

maintenance_count = len(
    df[df["Status"].str.lower() == "maintenance"]
)

overdue_count = len(
    assets_due_for_maintenance(df)
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Assets", total_assets)

with col2:
    st.metric("Active Assets", active_count)

with col3:
    st.metric("Under Maintenance", maintenance_count)

with col4:
    st.metric("Overdue Maintenance", overdue_count)

st.divider()

# --------------------------------------------------
# Chat History
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if isinstance(message["content"], pd.DataFrame):

            st.dataframe(
                message["content"],
                use_container_width=True
            )

        else:

            st.write(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input("Ask a question about your assets...")

# --------------------------------------------------
# Process Question
# --------------------------------------------------

if prompt:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response

    answer = process_question(df, prompt)

    # Display assistant response

    with st.chat_message("assistant"):

        if isinstance(answer, pd.DataFrame):

            if answer.empty:

                st.write("No matching assets were found.")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": "No matching assets were found."
                    }
                )

            else:

                st.write(
                    f"I found {len(answer)} matching asset(s)."
                )

                st.dataframe(
                    answer,
                    use_container_width=True
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

        else:

            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )
