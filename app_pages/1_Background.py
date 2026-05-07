import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Background")

st.title("Background")

with open("docs/report_sections/1-background.md") as f:
    content = f.read()
st.markdown(content)