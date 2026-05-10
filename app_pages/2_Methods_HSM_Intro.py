from pathlib import Path
import streamlit as st
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Methods: HSM Intro")
st.title("Methods: SPFs")

render_report_page("methods-hsm-intro.md", Path(__file__).resolve().parent.parent)