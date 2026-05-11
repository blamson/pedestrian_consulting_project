from pathlib import Path
import streamlit as st
from loguru import logger
from risk_estimation.streamlit_helpers import render_report_page

logger.info("[Streamlit Navigation] - Loading Page: Data Acquisition")
st.title("Data Acquisition")

render_report_page("5-data-acquisition.md", Path(__file__).resolve().parent.parent)