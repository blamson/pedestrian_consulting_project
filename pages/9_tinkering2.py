import streamlit as st
import polars as pl
# import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Tinkerin"
logger.info(f"[Streamlit Navigation] - Loading Page: {title}")
st.set_page_config(layout="wide")
st.title(title)

aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

helpers.build_sidebar_new(aadt_limit_table, include_years=True)

if st.session_state.developer_view:
    helpers.show_session_state()

results_df = risk_mod.build_results_df_new(spf_table, aadt_limit_table)

st.write(results_df)

# REDO TIME SWEEPS