import streamlit as st
from pathlib import Path
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Background")

st.title("Background")
render_report_page("1-background.md", Path(__file__).resolve().parent.parent)