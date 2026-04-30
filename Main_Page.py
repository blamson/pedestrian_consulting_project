import streamlit as st
import polars as pl
import numpy as np
import plotly.express as px
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers
# import src.risk_estimation

st.set_page_config(layout="wide")
st.title("Hello world")

results_table = helpers.load_data("data/results/results_2026-04-19.csv")
# st.dataframe(results_table, width='stretch')

spf_table = helpers.load_data("data/spfs.csv")

# st.markdown('## OOOO interactive')
st.sidebar.header("Intersection")
intersection = st.sidebar.selectbox(
    label="Please select an intersection",
    options=("Agate & Mesa", "Agate & 4th"),
    index=0,
)

if intersection == "Agate & Mesa":
    int_type = "3st"
    minor_road = "Mesa"
    # minor_aadt_percent = 0.166
    DEFAULT_TRAFFIC_PERCENT = 7.6
    # minor_aadt_percent = 0.076
else:
    int_type = "4st"
    minor_road = "4th"
    DEFAULT_TRAFFIC_PERCENT = 7.6
    # minor_aadt_percent = 0.076

aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
aadt_limits = aadt_limit_table.filter(pl.col("intersection_type") == int_type)
DEFAULT_MAJOR_AADT = 11000
MAX_MAJOR_AADT = aadt_limits["aadt_major"].item()

if "aadt_major" not in st.session_state:
    st.session_state.aadt_major = DEFAULT_MAJOR_AADT

if "minor_aadt_percent" not in st.session_state:
    st.session_state.minor_aadt_percent = DEFAULT_TRAFFIC_PERCENT

st.sidebar.header("Traffic Parameters")
st.sidebar.number_input(
    label=f"Agate Daily Traffic Volume (AADT) - Default: {DEFAULT_MAJOR_AADT} - Maximum: {MAX_MAJOR_AADT}",
    min_value=1,
    max_value=MAX_MAJOR_AADT,
    step=5000,
    value=DEFAULT_MAJOR_AADT,
    key="aadt_major"
)

st.sidebar.write("We approximate minor road volume using major/minor road proportions provided by SGM, try changing it!")
max_percent = aadt_limits["aadt_minor"].item() / st.session_state.aadt_major * 100
st.sidebar.slider(
    label=f"{minor_road} Traffic Percent - Default: {DEFAULT_TRAFFIC_PERCENT}%",
    min_value=0.01,
    max_value=max_percent,
    step=0.1,
    value=DEFAULT_TRAFFIC_PERCENT,
    key="minor_aadt_percent",
    format="%.1f"
)

st.session_state.aadt_minor = round(st.session_state.aadt_major * st.session_state.minor_aadt_percent / 100, 2)

st.sidebar.header("Other Parameters")
years = st.sidebar.number_input(
    label="Select number of years for long run probability",
    min_value=1,
    max_value=100,
    value=10,
    key="years"
)

st.sidebar.header("Intersection Treatments")
twltl_cmf = st.sidebar.checkbox(
    label="Two Way Left Turn Lane",
    value=True
)
lighting_cmf = st.sidebar.checkbox(
    label="Street Lights (not traffic signals)",
    value=True
)
bulbout_cmf = st.sidebar.checkbox(
    label="Curb Extension (Bulbout)",
    value=False
)

signal_cmf = False
if int_type not in ["3sg", "4sg"]:  
    signal_cmf = st.sidebar.checkbox(
        label="Traffic Signal",
        value=False
    )

school_cmf = st.sidebar.checkbox(
    label="Nearby School",
    value=False
    )

baseline_results = risk_mod.estimate_crashes(
    spfs=spf_table, 
    int_name=intersection,
    int_type=int_type,
    aadt_major=st.session_state.aadt_major,
    aadt_minor=st.session_state.aadt_minor,
    aadt_max=aadt_limit_table,
    years=years
)

results = risk_mod.estimate_crashes(
    spfs=spf_table, 
    int_name=intersection,
    int_type=int_type,
    aadt_major=st.session_state.aadt_major,
    aadt_minor=st.session_state.aadt_minor,
    aadt_max=aadt_limit_table,
    twltl_cmf=twltl_cmf,
    bulbout_cmf=bulbout_cmf,
    lighting_cmf=lighting_cmf,
    signal_cmf=signal_cmf,
    school_cmf=school_cmf,
    years=years
)

st.sidebar.header("Developer Controls")
developer_view = st.sidebar.checkbox(
    label="Show detailed outputs and logs",
    value=True
)

if developer_view:
    col1, col2 = st.columns(2)

    col1.header("Results - Baseline")
    col1.write(baseline_results)

    col2.header("Results - Post Treatment")
    col2.write(results)


aadt_sweep_results = risk_mod.sweep_aadt_major(
    spf_table,
    int_name=intersection,
    int_type=int_type,
    aadt_max=aadt_limit_table,
    aadt_major_min = 1,
    # aadt_major_max = MAX_MAJOR_AADT,
    aadt_major_max=st.session_state.aadt_major,
    years=years,
    k=st.session_state.minor_aadt_percent / 100,
    twltl_cmf=twltl_cmf,
    bulbout_cmf=bulbout_cmf,
    lighting_cmf=lighting_cmf,
    signal_cmf=signal_cmf,
    school_cmf=school_cmf
)

st.header("Testing value sweeps")
col1, col2 = st.columns(2)

col1.header(f"{years} Year Crash Probability as Traffic Volume Increases")
# st.dataframe(results)
fig = px.area(aadt_sweep_results, x="aadt_major", y=f"{years}_year_crash_probability")
fig.update_layout(yaxis_range=[0,1])
col1.write(fig)

col2.header(f"How {minor_road} Volume Increases With Agate Volume")
proportions = [0.076, 0.164]
fig = px.area(aadt_sweep_results, x="aadt_major", y="aadt_minor")
fig.update_layout(yaxis_range=[0, aadt_limits["aadt_minor"].item()])
col2.write(fig)

st.header("Testing alternate sweeping function")

test = risk_mod.sweep_estimates(
    spfs=spf_table,
    int_name=intersection,
    int_type=int_type,
    aadt_max=aadt_limit_table,
    aadt_major_vals=[st.session_state.aadt_major],
    k_vals=[st.session_state.minor_aadt_percent / 100],
    years_vals=np.arange(1, years+1, 1),
    twltl_cmf=twltl_cmf,
    bulbout_cmf=bulbout_cmf,
    lighting_cmf=lighting_cmf,
    signal_cmf=signal_cmf,
    school_cmf=school_cmf
)

fig = px.area(test, x="years", y="long_run_ped_prob")
fig.update_layout(yaxis_range=[0, 1])
st.write(fig)

if developer_view:
    st.write(test)