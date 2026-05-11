import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Limitations")

st.title("Limitations")

with open("docs/report_sections/7-limitations.md") as f:
    content = f.read()
st.markdown(content)