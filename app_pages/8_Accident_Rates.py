import streamlit as st
from risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger
import polars as pl

title = "Accident Rates"
logger.info(f"[Streamlit Navigation] - Loading Page: {title}")

st.set_page_config(layout="wide")
st.title(title)

st.header("Expected Accidents Per Year")
# Data
aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

# Sidebar
intersection, inputs = helpers.build_sidebar(
    aadt_limit_table,
    include_years=False
)

# Load original results
original_results = (
    helpers.load_data("data/results/results_2026-05-07.csv")
    .filter(pl.col("intersection_name") == intersection.name)
)

# Debug info
if inputs.developer_view:
    helpers.show_debug(intersection, inputs)

# Results computation
results_df = risk_mod.build_results_df(
    spf_table=spf_table,
    intersection=intersection,
    inputs=inputs,
    aadt_limit_table=aadt_limit_table
)

# Visualization

tab1, tab2, tab3, tab4 = st.tabs([
    "Chart - Selected Values",
    "Chart - Default Values",
    "Data - Selected Values",
    "Data - Default Values"
])

with tab1:
    plotting_helpers.render_charts(results_df, "selected")

with tab2:
    plotting_helpers.render_charts(original_results, "default")

with tab3:
    st.write(results_df.drop(["long_run_ped_prob", "years"]))

with tab4:
    st.write(original_results.drop(["long_run_ped_prob", "years"]))
    
text = helpers.load_text("app_pages/text_files/dashboard/accidents-per-year.md")
estimation_text = helpers.load_text("app_pages/text_files/dashboard/estimation-methods.md")

if intersection.name == "Agate & 4th":
    if st.toggle("Show direct estimation explanation?"):
        st.markdown(estimation_text)

if st.toggle("Show explanation?"):
    st.markdown(text)
