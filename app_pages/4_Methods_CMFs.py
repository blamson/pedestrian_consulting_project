from pathlib import Path
import streamlit as st
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Methods: CMFs")
st.title("Methods: Crash Modification Factors (CMFs)")

render_report_page("methods-cmfs.md", Path(__file__).resolve().parent.parent)