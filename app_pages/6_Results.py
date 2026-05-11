from pathlib import Path
import streamlit as st
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Results and Interpretation")

st.title("Results and Interpretation")

render_report_page("6-results.md", Path(__file__).resolve().parent.parent)