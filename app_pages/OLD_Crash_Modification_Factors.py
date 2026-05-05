import streamlit as st

st.set_page_config(
    page_title="Crash Modification Factors"
)

with open("docs/notes/hsm-crash-modification-factors.md") as f:
    writeup = f.read()

st.markdown(writeup)