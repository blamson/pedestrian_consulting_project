import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Methodology")

st.title("Methodology")

with open("docs/report_sections/2-methodology.md") as f:
    content = f.read()
st.markdown(content)