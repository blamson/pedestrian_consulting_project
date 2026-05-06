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

helpers.build_sidebar_new(aadt_limit_table, include_years=False)

if st.session_state.developer_view:
    helpers.show_session_state()

results_df = risk_mod.build_results_df_new(spf_table, aadt_limit_table)

st.write(results_df)

st.header("Expected Accidents Per Year")
text = helpers.load_text("pages/text_files/main_page/accidents-per-year.md")
st.markdown(text)

col1, col2 = st.columns(2)
tab11, tab12 = col1.tabs(["Chart", "Data"])
tab21, tab22 = col2.tabs(["Chart", "Data"])
fig1, key1 = plotting_helpers.make_accident_bar_new(
    results_df,
    y_col="pred_ped",
    title="Pedestrian Accident Rate",
    y_label="Accidents per Year",
    key="pedestrian_accident_rate_plot"
)

fig2, key2 = plotting_helpers.make_accident_bar_new(
    results_df,
    y_col="pred_veh",
    title="Vehicle Accident Rate",
    y_label="Accidents per Year",
    key="vehicle_accident_rate_plot"
)

tab11.plotly_chart(fig1, key=key1)
tab12.write(results_df.drop(["intersection_name", "intersection_type", "pred_veh", "long_run_ped_prob", "years"]))
tab21.plotly_chart(fig2, key=key2)
tab22.write(results_df.drop(["intersection_name", "intersection_type", "pred_ped", "long_run_ped_prob", "years"]))