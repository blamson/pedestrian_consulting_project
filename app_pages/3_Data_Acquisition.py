import streamlit as st
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Data Acquisition")

st.title("Data Acquisition")

with open("docs/report_sections/3-data-acquisition.md") as f:
    content = f.read()
st.markdown(content)