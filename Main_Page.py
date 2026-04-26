import streamlit as st
import polars as pl
from src.risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers
# import src.risk_estimation

st.title("Hello world")

results_table = helpers.load_data("data/results/results_2026-04-19.csv")
st.dataframe(results_table, width='stretch')

spf_table = helpers.load_data("data/spfs.csv")

# st.markdown('## OOOO interactive')
intersection = st.selectbox(
    label="Please select an intersection",
    options=("Agate & Mesa", "Agate & 4th"),
    index=0,
)

if intersection == "Agate & Mesa":
    int_type = "3st"
    minor_road = "Mesa"
    # minor_aadt_prop = 0.166
    minor_aadt_prop = 0.076
else:
    int_type == "4st"
    minor_road = "4th"
    minor_aadt_prop = 0.076

aadt_limit_table = helpers.load_data("data/aadt_maximums.csv")
aadt_limits = aadt_limit_table.filter(pl.col("intersection_type") == int_type)
DEFAULT_MAJOR_AADT = 11000
MAX_MAJOR_AADT = aadt_limits["aadt_major"].item()

if "aadt_major" not in st.session_state:
    st.session_state.aadt_major = DEFAULT_MAJOR_AADT

# if "aadt_minor" not in st.session_state:
#     st.session_state.aadt_minor = 

st.number_input(
    label=f"Agate Daily Traffic Volume (AADT) - Default: {DEFAULT_MAJOR_AADT} - Maximum: {MAX_MAJOR_AADT}",
    min_value=1,
    max_value=MAX_MAJOR_AADT,
    value=DEFAULT_MAJOR_AADT,
    key="aadt_major"
)

st.session_state.aadt_minor = st.session_state.aadt_major * minor_aadt_prop

results = risk_mod.estimate_crashes(
    spfs=spf_table, 
    int_name=intersection,
    int_type=int_type,
    aadt_major=st.session_state.aadt_major,
    aadt_minor=st.session_state.aadt_minor,
    aadt_max=aadt_limit_table
)

st.write(results)
# st.write(spf_table)