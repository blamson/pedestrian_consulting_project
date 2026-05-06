import streamlit as st
import polars as pl
# import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Accident Rates"
logger.info(f"[Streamlit Navigation] - Loading Page: {title}")
st.set_page_config(layout="wide")
st.title(title)

# Data loading ---
# results_table = helpers.load_data("data/results/results_2026-04-19.csv") # currently unused, will be important for pre-set scenarios?
aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

# Sidebar Creation ---
config = helpers.build_sidebar(aadt_limit_table)

results_df = risk_mod.build_results_df(spf_table, aadt_limit_table, config)

if config["developer_view"]:
    st.write(results_df)

# CRASH RATES SECTION ------
st.header("Expected Accidents Per Year")
text = helpers.load_text("pages/text_files/main_page/accidents-per-year.md")
st.markdown(text)

figcol1, figcol2 = st.columns(2)
color_map = {
    "baseline": "#4C78A8",
    "post-treatment": "#F58518"
}
fig1, key1 = plotting_helpers.make_accident_bar(
    results_df,
    y_col="pred_ped",
    title="Pedestrian Accident Rate",
    y_label="Accidents per Year",
    color_map=color_map,
    key="pedestrian_accident_rate_plot"
)

fig2, key2 = plotting_helpers.make_accident_bar(
    results_df,
    y_col="pred_veh",
    title="Vehicle Accident Rate",
    y_label="Accidents per Year",
    color_map=color_map,
    key="vehicle_accident_rate_plot"
)

figcol1.plotly_chart(fig1, key=key1)
figcol2.plotly_chart(fig2, key=key2)