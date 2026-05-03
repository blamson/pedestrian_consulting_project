import streamlit as st
import polars as pl
from typing import List, Dict
from loguru import logger


@st.cache_data
def load_data(path):
    df = pl.read_csv(path)
    return df


@st.cache_data
def combine_results(results: List[Dict]) -> pl.DataFrame:
    return pl.DataFrame(results)


# @st.cache_data
def load_text(path):
    text = ""
    with open(path) as f:
        text = f.read()
    
    return text


def build_sidebar(aadt_limit_table: pl.DataFrame):
    logging_context = "Streamlit Sidebar"
    logger.info(f"[{logging_context}] - Building Sidebar")
    st.sidebar.header("Intersection")

    intersection = st.sidebar.selectbox(
        "Please select an intersection",
        ("Agate & Mesa", "Agate & 4th"),
        index=0
    )

    # --- Intersection-specific config ---
    if intersection == "Agate & Mesa":
        int_type = "3st"
        minor_road = "Mesa"
        DEFAULT_TRAFFIC_PERCENT = 7.6
        bulbout=True
    else:
        int_type = "4st"
        minor_road = "4th"
        DEFAULT_TRAFFIC_PERCENT = 7.6
        bulbout=False

    aadt_limits = aadt_limit_table.filter(
        pl.col("intersection_type") == int_type
    )

    DEFAULT_MAJOR_AADT = 11000
    MAX_MAJOR_AADT = aadt_limits["aadt_major"].item()

    # --- Session state init ---
    if "aadt_major" not in st.session_state:
        st.session_state.aadt_major = DEFAULT_MAJOR_AADT

    if "minor_aadt_percent" not in st.session_state:
        st.session_state.minor_aadt_percent = DEFAULT_TRAFFIC_PERCENT

    # --- Traffic inputs ---
    st.sidebar.header("Traffic Parameters")
    help_text = load_text("pages/text_files/help_text/aadt_major.txt")
    st.sidebar.number_input(
        label=f"Agate Traffic Volume - Default: {DEFAULT_MAJOR_AADT} - Max: {MAX_MAJOR_AADT}",
        min_value=1,
        max_value=MAX_MAJOR_AADT,
        value=DEFAULT_MAJOR_AADT,
        step=5000,
        key="aadt_major",
        help=help_text
    )

    help_text = load_text("pages/text_files/help_text/minor_percent.txt")
    st.sidebar.slider(
        label=f"{minor_road} Traffic Percent",
        min_value=0.01,
        max_value=99.00,
        step=0.1,
        value=DEFAULT_TRAFFIC_PERCENT,
        key="minor_aadt_percent",
        format="%.1f",
        help=help_text
)

    aadt_minor = round(
        st.session_state.aadt_major
        * st.session_state.minor_aadt_percent / 100,
        2
    )

    st.sidebar.write(f"{minor_road} Traffic Volume: {int(aadt_minor)}")

    if aadt_minor > aadt_limits["aadt_minor"].item():
        st.sidebar.warning(f"Minor road volume exceeds limit of {aadt_limits["aadt_minor"].item()} supported by traffic model, results will be less reliable.")

    # --- Other params ---
    st.sidebar.header("Other Parameters")
    help_text = load_text("pages/text_files/help_text/years.txt")
    years = st.sidebar.number_input(
        "Years",
        min_value=1,
        max_value=100,
        value=10,
        key="years",
        help=help_text
    )

    # --- Treatments ---
    st.sidebar.header("Intersection Treatments")

    twltl = st.sidebar.checkbox("Two Way Left Turn Lane", value=True, help=load_text("pages/text_files/help_text/twltl.txt"))
    lighting = st.sidebar.checkbox("Street Lights", True, help=load_text("pages/text_files/help_text/street_lights.txt"))
    bulbout = st.sidebar.checkbox("Bulbout", bulbout, help=load_text("pages/text_files/help_text/bulbout.txt"))

    signal = False
    disabled = True
    if int_type == "4st":
        disabled = False
    signal = st.sidebar.checkbox("Traffic Signal", signal, help=load_text("pages/text_files/help_text/traffic_signal.txt"), disabled=disabled)

    school = False
    if int_type in ["3sg", "4sg"]:
        school = st.sidebar.checkbox("Nearby School", False)

    # --- Dev controls ---
    st.sidebar.header("Developer Controls")
    developer_view = st.sidebar.checkbox(
        "Show detailed outputs and logs",
        value=False
    )
    if developer_view:
        logger.info(f"[{logging_context}] - Enabling Developer Output")

    # --- Return structured config ---
    return {
        "intersection": intersection,
        "int_type": int_type,
        "minor_road": minor_road,
        "aadt_major": st.session_state.aadt_major,
        "aadt_minor": aadt_minor,
        "minor_percent": st.session_state.minor_aadt_percent / 100,
        "years": years,
        "cmf": {
            "twltl_cmf": twltl,
            "lighting_cmf": lighting,
            "bulbout_cmf": bulbout,
            "signal_cmf": signal,
            "school_cmf": school,
        },
        "developer_view": developer_view,
        "aadt_limits": aadt_limits,
    }
