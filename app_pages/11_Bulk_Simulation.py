import streamlit as st
import polars as pl
import plotly.express as px
from risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Simulating Long Term Risk - Large Simulation"
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

# Debug info
if inputs.developer_view:
    helpers.show_debug(intersection, inputs)

# Results computation
results_df = (
    risk_mod.build_results_df(
        spf_table=spf_table,
        intersection=intersection,
        inputs=inputs,
        aadt_limit_table=aadt_limit_table
    )
)

n_trials = st.number_input(
    label="Number of Simulations",
    min_value=1,
    value=10000,
    step=1000,
    max_value=100000
)
simulation_results = risk_mod.simulate_accidents_bulk(results_df, n_trials=int(n_trials))

scenario_order = results_df["scenario"].to_list()
fig, key = plotting_helpers.make_accident_bar(
    df=simulation_results,
    title=f"Breakdown of crashes over {n_trials} simulated {inputs.years} year periods",
    y_col="probability",
    y_label="Percent of trials (%)",
    x_col="simulated_total_crashes",
    x_label=f"Number of crashes in {inputs.years} years",
    key="bulk_simulation_plot",
    scenario_order=scenario_order,
    barmode="group",
    legend=True,
    rounding_format=":.2f"
)
fig.update_layout(
    xaxis_ticksuffix=" crashes"
)
fig.update_traces(
    hovertemplate=(
        "Crashes: %{x}<br>"
        "Probability: %{y:.2f}<br>"
        "Count: %{customdata}"
        "<extra></extra>"
    ),
    customdata=simulation_results["count"]
)

st.plotly_chart(fig)

text = helpers.load_text("app_pages/text_files/dashboard/bulk-simulations.md")
if st.toggle("Show explanation?"):
    st.markdown(text)