import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Results and Interpretation")

st.title("Results and Interpretation")

with open("docs/report_sections/4-results.md") as f:
    content = f.read()
st.markdown(content)