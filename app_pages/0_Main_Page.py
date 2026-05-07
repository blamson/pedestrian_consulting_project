import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Main Page")

st.title("Granby Pedestrian Consulting Project")

with open("docs/executive-summary.md") as f:
    summary = f.read()
st.markdown(summary)

st.markdown("---")
st.info("Use the sidebar to navigate to the **Dashboard**, **Writeup**, **Crash Modification Factors**, and **HSM Notes** pages.")