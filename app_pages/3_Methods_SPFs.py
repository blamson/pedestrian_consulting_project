from pathlib import Path
import streamlit as st
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Methods: SPFs")
st.title("Methods: Safety Performance Functions (SPFs)")

render_report_page("3-methods-spfs.md", Path(__file__).resolve().parent.parent)