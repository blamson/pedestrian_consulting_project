import streamlit as st
import polars as pl
import plotly.express as px
from risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Long Term Risk"
logger.info(f"[Streamlit Navigation] - Loading Page: {title}")
st.set_page_config(layout="wide")
st.title(title)

# Data 
aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

# Sidebar
intersection, inputs = helpers.build_sidebar(
    aadt_limit_table,
    include_years=True
)

# Load original results
original_results = (
    helpers.load_data("data/results/sweep_results_2026-05-07.csv")
    .filter(pl.col("intersection_name") == intersection.name)
)

# Debug info
if inputs.developer_view:
    helpers.show_debug(intersection, inputs)

# Results computation
results_df = (
    risk_mod.build_results_df(
        spf_table=spf_table,
        intersection=intersection,
        inputs=inputs,
        aadt_limit_table=aadt_limit_table,
        sweep_century=True
    )
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Chart - Selected Values",
    "Chart - Default Values",
    "Data - Selected Values",
    "Data - Default Values"
])

with tab1:
    plotting_helpers.render_long_term_risk(results_df, "selected", inputs.years)

with tab2:
    plotting_helpers.render_long_term_risk(original_results, "default", inputs.years)

with tab3:
    st.write(results_df)

with tab4:
    st.write(original_results)

text = helpers.load_text("app_pages/text_files/dashboard/long-term-risk.md")
if st.toggle("Show explanation?"):
    st.markdown(text)