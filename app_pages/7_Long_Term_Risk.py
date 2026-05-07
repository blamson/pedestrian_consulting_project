import streamlit as st
import polars as pl
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers
from loguru import logger

title = "Tinkerin"
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
        aadt_limit_table=aadt_limit_table,
        sweep_century=True
    )
)

text = helpers.load_text("app_pages/text_files/dashboard/long-term-risk.md")
st.markdown(text)

tab1, tab2 = st.tabs(["Chart - Selected Values", "Data"])
col1, col2 = tab1.columns(2)

fig = px.bar(
    results_df.filter(pl.col("years") == inputs.years), 
    x="scenario", 
    y="long_run_ped_percent", 
    text="long_run_ped_percent",
    title=f"Chance of at least one accident in {inputs.years} years",
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
col1.plotly_chart(fig, key="long_term_risk_plot")

fig = px.line(
    results_df, 
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
fig.add_vline(x=inputs.years, line_width=1, line_dash="dash", line_color="red", opacity=0.7, annotation_text=f"Year Selected: {inputs.years}")
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
col2.plotly_chart(fig, key="year_line_plot")

tab2.write(results_df)