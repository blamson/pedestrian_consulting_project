import streamlit as st
import polars as pl
import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

logger.info("[Streamlit Navigation] - Loading Page: Main Page")
st.set_page_config(layout="wide")
st.title("Interactive Dashboad")

# Data loading ---
# results_table = helpers.load_data("data/results/results_2026-04-19.csv") # currently unused, will be important for pre-set scenarios?
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

# LONG TERM RISK SECTION -------
st.header("Long term pedestrian risk")
text = helpers.load_text("pages/text_files/main_page/long-term-risk.md")
st.markdown(text)
years_figcol1, years_figcol2 = st.columns(2)

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
    marker=dict(color=px.colors.qualitative.Vivid)
)
fig.update_layout(yaxis_range=[0, 100])
years_figcol1.plotly_chart(fig, key="long_term_risk_plot")

# LONG TERM RISK - YEAR SWEEP SECTION 
baseline_year_sweep = risk_mod.sweep_across_years(
    spfs=spf_table,
    int_name=config["intersection"],
    int_type=config["int_type"],
    aadt_major=config["aadt_major"],
    aadt_minor=config["aadt_minor"],
    aadt_max=aadt_limit_table,
    scenario_name="baseline"
)

post_year_sweep = risk_mod.sweep_across_years(
    spfs=spf_table,
    int_name=config["intersection"],
    int_type=config["int_type"],
    aadt_major=config["aadt_major"],
    aadt_minor=config["aadt_minor"],
    aadt_max=aadt_limit_table,
    scenario_name="post-treatment",
    **config["cmf"]
)

year_sweep_df = (
    pl.concat([baseline_year_sweep, post_year_sweep])
    .with_columns(long_run_ped_percent=pl.col("long_run_ped_prob")*100)
    .with_columns(long_run_ped_percent=pl.col("long_run_ped_percent").round(2))
)

fig = px.line(
    year_sweep_df, 
    x="years", 
    y="long_run_ped_percent", 
    color="scenario",
    title="Chance of at least one accident over time",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    labels={
        "years": "Years",
        "scenario": "Scenario",
        "long_run_ped_percent": "Chance of an accident (%)"
    }
)
fig.add_vline(x=config["years"], line_width=1, line_dash="dash", line_color="red", annotation_text=f"Years Selected: {config["years"]}")
fig.update_traces(
    marker=dict(color=[color_map[s] for s in results_df["scenario"]])
)
fig.update_layout(yaxis_range=[0, 100])
years_figcol2.plotly_chart(fig, key="year_line_plot")