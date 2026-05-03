import streamlit as st
import polars as pl
import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Main Draft")
st.set_page_config(layout="wide")
st.title("Interactive Dashboad")

# Data loading ---
results_table = helpers.load_data("data/results/results_2026-04-19.csv")
aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

# Sidebar Creation ---
config = helpers.build_sidebar(aadt_limit_table)

baseline_results = risk_mod.estimate_crashes(
    spfs=spf_table,
    int_name=config["intersection"],
    int_type=config["int_type"],
    aadt_major=config["aadt_major"],
    aadt_minor=config["aadt_minor"],
    aadt_max=aadt_limit_table,
    years=config["years"],
    scenario_name="baseline"
)

results = risk_mod.estimate_crashes(
    spfs=spf_table,
    int_name=config["intersection"],
    int_type=config["int_type"],
    aadt_major=config["aadt_major"],
    aadt_minor=config["aadt_minor"],
    aadt_max=aadt_limit_table,
    years=config["years"],
    scenario_name="post-treatment",
    **config["cmf"]
)

results_df = (
    helpers.combine_results([baseline_results, results])
    .with_columns(long_run_ped_percent=pl.col("long_run_ped_prob")*100)
    .with_columns(long_run_ped_percent=pl.col("long_run_ped_percent").round(2))
)

col1, col2 = st.columns(2)
if config["developer_view"]:

    col1.header("Results - Baseline")
    col1.write(baseline_results)

    col2.header("Results - Post Treatment")
    col2.write(results)

    st.write(results_df)


# CRASH RATES SECTION ------
st.header("Expected Accidents Per Year")
st.markdown(
    """
    The main numbers our process outputs is a rate. It's the expected number of accidents per year. We want to be careful when interpreting this value.

    A large number doesn't mean a lot of accidents **will** happen, and a small number doesn't mean a lot of accidents **cant** happen.
    It's all random, and our goal is not to precisely forecast crashes per year. For the context of this project, the rate works more as a loose proxy for risk. We care more about how much this rate changes between scenarios.

    These rates can be awkward to interpret, especially when they're smaller than 1 which is common for pedestrian accidents. In that case you can think of it as how many years it would take for that number to add up to one. 

    Here is an example: An excepted number of 0.2 accidents per year? That'd be one expected accident in 5 years. 

    #### Notes

    Notice how some treatments (like the traffic signal) effect both pedestrian and vehicle rates, and others (like the bulbout) effect only the pedestrian rates. Crash Modification Factors can be very narrow in the context that they apply to! 
    """
)

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

# st.markdown(
#     """
#     ### Pedestrian Accidents - Indirect vs. Direct Estimation
    
#     There are two methods we use to get our pedestrian rates. 
    
#     1. Direct Estimation: Uses a model specifically made for estimating pedestrian rates. This model takes in traffic volume alongside pedestrian volume and the number of lanes.
#     2. Indirect Estimation: Uses a model for vehicle accident rates and assumes pedestrian crashes will make up around 2\% of those crashes. 

#     Direct estimation is better
#     """
# )

# LONG TERM RISK SECTION -------
st.header("Long term pedestrian risk")
st.markdown(
    """
    This plot shows how the estimated chance of **at least one** pedestrian-involved crash in a given period changes as traffic conditions change.

    - Use the sidebar controls to modify the **traffic parameters** 
        - Traffic volume is the primary driver of risk, try maxing it out to see how much the line rises. 

    - **Intersection treatments** can also be compared here
        - The baseline scenario will always stay the same so try selecting and de-selecting the various options to see what impact they have! 
    """
)
fig = px.bar(
    results_df, 
    x="scenario", 
    y="long_run_ped_percent", 
    text="long_run_ped_percent",
    title=f"Chance of at least one accident in {config["years"]} years",
    labels={
        "scenario": "Scenario",
        "long_run_ped_percent": "Chance of an accident (%)"
    }
)
fig.update_traces(
    textposition="outside",
    texttemplate="%{text:.0f}%",
    marker=dict(color=[color_map[s] for s in results_df["scenario"]])
)
# fig.update_yaxes(rangemode="tozero")
fig.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig, key="long_term_risk_plot")