import streamlit as st
import polars as pl
# import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Long Term Risk"
logger.info(f"[Streamlit Navigation] - Loading Page: {title}")
st.set_page_config(layout="wide")
st.title(title)

aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
spf_table = helpers.load_data("data/spfs.csv")

config = helpers.build_sidebar(aadt_limit_table)

results_df = risk_mod.build_results_df(spf_table, aadt_limit_table, config)

if config["developer_view"]:
    st.write(results_df)

text = helpers.load_text("pages/text_files/main_page/long-term-risk.md")
st.markdown(text)
years_figcol1, years_figcol2 = st.columns(2)

fig = px.bar(
    results_df, 
    x="scenario", 
    y="long_run_ped_percent", 
    text="long_run_ped_percent",
    title=f"Chance of at least one accident in {config['years']} years",
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
    scenario_name="baseline",
    pedvol=config["pedvol"],
    nlanes=config["nlanes"]
)

post_year_sweep = risk_mod.sweep_across_years(
    spfs=spf_table,
    int_name=config["intersection"],
    int_type=config["int_type"],
    aadt_major=config["aadt_major"],
    aadt_minor=config["aadt_minor"],
    aadt_max=aadt_limit_table,
    scenario_name="post-treatment",
    pedvol=config["pedvol"],
    nlanes=config["nlanes"],
    **config["cmf"]
)

if config["intersection"] == "Agate & 4th":
    post_year_sweep_direct = risk_mod.sweep_across_years(
        spfs=spf_table,
        int_name=config["intersection"],
        int_type="4sg",
        aadt_major=config["aadt_major"],
        aadt_minor=config["aadt_minor"],
        aadt_max=aadt_limit_table,
        scenario_name="post-treatment-direct",
        pedvol=config["pedvol"],
        nlanes=config["nlanes"]
    )

    tables_to_combine = [baseline_year_sweep, post_year_sweep, post_year_sweep_direct]

else:
    tables_to_combine = [baseline_year_sweep, post_year_sweep]

year_sweep_df = (
    pl.concat(tables_to_combine)
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
fig.add_vline(x=config["years"], line_width=1, line_dash="dash", line_color="red", opacity=0.7, annotation_text=f"Year Selected: {config['years']}")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(
    yaxis_range=[0, 100],
    legend=dict(
        yanchor="bottom",
        y=0.01,
        xanchor="right",
        x=0.99
    ),
    hovermode="x"
)
fig.update_xaxes(showspikes=True, spikemode="across", spikethickness=1, spikecolor="grey")
# fig.update_yaxes(showspikes=True, spikemode="across", spikethickness=2, spikecolor="grey")
years_figcol2.plotly_chart(fig, key="year_line_plot")