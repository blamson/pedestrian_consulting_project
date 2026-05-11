import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Main Page")

st.title("Granby Pedestrian Consulting Project")

with open("docs/report_sections/executive-summary.md") as f:
    summary = f.read()
st.markdown(summary)
