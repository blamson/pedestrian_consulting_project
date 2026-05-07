import streamlit as st
import polars as pl
from typing import List, Dict
from loguru import logger

@st.cache_data
def load_data(path: str) -> pl.DataFrame:
    df = pl.read_csv(path)
    return df


@st.cache_data
def combine_results(results: List[Dict]) -> pl.DataFrame:
    return pl.DataFrame(results)


@st.cache_data
def load_text(path: str) -> str:
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
        disable_minor_volume = False
        disable_direct_estimation = True
    else:
        int_type = "4st"
        minor_road = "4th"
        DEFAULT_TRAFFIC_PERCENT = 7.6
        bulbout=False
        disable_minor_volume = True
        disable_direct_estimation = False
        signal=True


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
        help=help_text,
        disabled=disable_minor_volume
    )
    if disable_minor_volume:
        st.sidebar.warning("Minor volume adjustment available only for Agate & Mesa.")

    aadt_minor = round(
        st.session_state.aadt_major
        * st.session_state.minor_aadt_percent / 100,
        2
    )

    st.sidebar.write(f"{minor_road} Traffic Volume: {int(aadt_minor)}")

    if aadt_minor > aadt_limits["aadt_minor"].item():
        st.sidebar.warning(f"Minor road volume exceeds limit of {aadt_limits['aadt_minor'].item()} supported by traffic model, results will be less reliable.")

    # --- Other params ---
    st.sidebar.header("Other Parameters")
    years = st.sidebar.number_input(
        "Years",
        min_value=1,
        max_value=100,
        value=10,
        key="years",
        help=load_text("pages/text_files/help_text/years.txt")
    )

    st.sidebar.header("Direct Estimation Parameters", help="Direct estimation only available for Agate & 4th")
    pedvol = st.sidebar.number_input(
        label="Daily Pedestrian Volume",
        min_value=1,
        max_value=1000,
        value=138,
        step=100,
        key="pedvol",
        disabled=disable_direct_estimation,
        help=load_text("pages/text_files/help_text/pedvol.txt")
    )
    nlanes = st.sidebar.number_input(
        label="Number of Lanes",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="nlanes",
        disabled=disable_direct_estimation,
        help=load_text("pages/text_files/help_text/nlanes.txt")
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
        signal=True
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
        "nlanes": nlanes,
        "pedvol": pedvol,
        "developer_view": developer_view,
        "aadt_limits": aadt_limits,
    }

# NEW SIDEBAR CODE SECTION WOOOOO --------------
def sync_selected_with_intersection():
    cfg = st.session_state._active_config

    prev_intersection = st.session_state.get("_last_intersection")
    current_intersection = st.session_state.intersection

    # only reset when intersection actually changes
    if prev_intersection != current_intersection:
        st.session_state.minor_pct_selected = cfg["minor_pct_default"]
        st.session_state.aadt_major_selected = 11000
        st.session_state.pedvol_selected = cfg["pedvol_default"]
        st.session_state.nlanes_selected = cfg["nlanes_default"]
        st.session_state.bulbout_cmf = cfg["bulbout_default"]
        st.session_state.signal_cmf = cfg["signal_default"]

        st.session_state._last_intersection = current_intersection


def init_intersection_config() -> None:
    st.sidebar.header("Intersection")

    intersection = st.sidebar.selectbox(
        "Please select an intersection",
        ("Agate & Mesa", "Agate & 4th"),
        key="intersection"
    )

    if intersection == "Agate & Mesa":
        config = dict(
            int_type_default="3st",
            int_type_alt=None,
            minor_road="Mesa",
            minor_pct_default=3.2,    # From 6th after diversion - Lower bound
            minor_pct_alt=16.6,       # From 6th before diversion - Upper bound
            bulbout_default=True,
            disable_minor_volume=False,
            disable_direct_estimation=True,
            signal_default=False,
            pedvol_default=138.4,     # Not used for mesa, but included incase future development requires it
            nlanes_default=5,         # Not used for mesa, but included incase future development requires it
        )
    else:
        config = dict(
            int_type_default="4st",
            int_type_alt="4sg",
            minor_road="4th",
            minor_pct_default=7.6,
            minor_pct_alt=12.6,
            bulbout_default=False,
            disable_minor_volume=True,
            disable_direct_estimation=False,
            signal_default=True,
            pedvol_default=145.32,
            nlanes_default=5
        )

    # persist config
    for k, v in config.items():
        st.session_state[k] = v

    st.session_state._active_config = config
        

def init_aadt_limits(
    aadt_limit_table: pl.DataFrame
) -> None:
    aadt_limits_default = aadt_limit_table.filter(pl.col("intersection_type") == st.session_state.int_type_default)
    aadt_limits_alt = aadt_limit_table.filter(pl.col("intersection_type") == st.session_state.int_type_alt)

    st.session_state.max_aadt_major_default = aadt_limits_default["aadt_major"].item()
    st.session_state.max_aadt_minor_default = aadt_limits_default["aadt_minor"].item()

    st.session_state.max_aadt_major_alt = None
    st.session_state.max_aadt_minor_alt = None
    if not aadt_limits_alt.is_empty():
        st.session_state.max_aadt_major_alt = aadt_limits_alt["aadt_major"].item()
        st.session_state.max_aadt_minor_alt = aadt_limits_alt["aadt_minor"].item()


    if "aadt_major_default" not in st.session_state:
        st.session_state.aadt_major_default = 11000

    if "minor_aadt_percent" not in st.session_state:
        st.session_state.minor_aadt_percent = st.session_state.minor_pct_default


def determine_max_aadt() -> int:
    if st.session_state.max_aadt_major_alt is not None:
        return max(st.session_state.max_aadt_major_default, st.session_state.max_aadt_major_alt)

    return st.session_state.max_aadt_major_default
    

def sidebar_traffic_inputs():
    st.sidebar.header("Traffic Parameters")

    st.sidebar.number_input(
        label="Agate Traffic Volume",
        min_value=1,
        max_value=determine_max_aadt(),
        step=5000,
        value=11000,
        key="aadt_major_selected",
        help=load_text("pages/text_files/help_text/aadt_major.txt"),
    )

    if st.session_state.disable_minor_volume:
        # st.sidebar.warning("Minor volume adjustment available only for Agate & Mesa.")
        st.session_state.minor_pct_selected = st.session_state.minor_pct_default

    st.sidebar.number_input(
        label=f"{st.session_state.minor_road} Traffic Percent",
        min_value=0.01,
        max_value=99.0,
        step=5.0,
        value=st.session_state.minor_pct_default,
        key="minor_pct_selected",
        format="%.1f",
        disabled=st.session_state.disable_minor_volume,
        help=load_text("pages/text_files/help_text/minor_percent.txt"),
    )


def calculate_minor_aadt(
    aadt_major: int,
    minor_percent: float,
    minor_limit,
    write_to_sidebar=False
) -> float:

    aadt_minor = round(aadt_major * minor_percent / 100, 2)

    if write_to_sidebar:

        if aadt_minor > minor_limit:
            st.sidebar.warning(
                f"Minor road volume exceeds limit of {minor_limit}, results may be unreliable."
            )
    
    return aadt_minor


def set_minor_aadt() -> None:

    # Default aadt
    minor_limit = st.session_state.max_aadt_minor_default
    st.session_state.minor_aadt_default = calculate_minor_aadt(
        st.session_state.aadt_major_default,
        st.session_state.minor_pct_default,
        minor_limit
    )

    # Alternative aadt
    if st.session_state.max_aadt_minor_alt is not None:
        minor_limit = st.session_state.max_aadt_minor_alt
    
    st.session_state.minor_aadt_alt = calculate_minor_aadt(
        st.session_state.aadt_major_default,
        st.session_state.minor_pct_alt,
        minor_limit
    )

    # Selected aadt
    st.session_state.minor_aadt_selected = calculate_minor_aadt(
        st.session_state.aadt_major_selected,
        st.session_state.minor_pct_selected,
        minor_limit=st.session_state.max_aadt_minor_default,
        write_to_sidebar=True
    )

    st.sidebar.metric(
        label=f"{st.session_state.minor_road} Traffic Volume - Default: {int(st.session_state.minor_aadt_default)}", 
        value=f"{int(st.session_state.minor_aadt_selected)} veh/day", 
        delta=f"{int(st.session_state.minor_aadt_selected) - int(st.session_state.minor_aadt_default)}, veh/day",
        border=True,
        help="Bottom value shows difference from default minor aadt"
    )


def sidebar_years():
    st.sidebar.header("Time Parameters")

    st.sidebar.number_input(
        "Years",
        min_value=1,
        max_value=100,
        key="years",
        value=10,
        help=load_text("pages/text_files/help_text/years.txt")
    )


def sidebar_direct_estimation():
    st.sidebar.header("Direct Estimation Parameters")

    st.sidebar.number_input(
        "Daily Pedestrian Volume",
        min_value=1,
        max_value=1000,
        step=100,
        value=int(st.session_state.pedvol_default),
        key="pedvol_selected",
        disabled=st.session_state.disable_direct_estimation,
        help=load_text("pages/text_files/help_text/pedvol.txt"),
    )

    st.sidebar.number_input(
        "Number of Lanes",
        min_value=1,
        max_value=10,
        step=1,
        value=st.session_state.nlanes_default,
        key="nlanes_selected",
        disabled=st.session_state.disable_direct_estimation,
        help=load_text("pages/text_files/help_text/nlanes.txt"),
    )


def sidebar_treatments():
    st.sidebar.header("Intersection Treatments")

    st.sidebar.checkbox(
        "Two Way Left Turn Lane",
        value=True,
        key="twltl_cmf",
        help=load_text("pages/text_files/help_text/twltl.txt"),
    )

    st.sidebar.checkbox(
        "Street Lights",
        value=True,
        key="lighting_cmf",
        help=load_text("pages/text_files/help_text/street_lights.txt"),
    )

    st.sidebar.checkbox(
        "Bulbout",
        value=st.session_state.bulbout_default,
        key="bulbout_cmf",
        help=load_text("pages/text_files/help_text/bulbout.txt"),
    )

    disabled = st.session_state.int_type_default != "4st"

    st.sidebar.checkbox(
        "Traffic Signal",
        value=st.session_state.signal_default,
        key="signal_cmf",
        disabled=disabled,
        help=load_text("pages/text_files/help_text/traffic_signal.txt"),
    )


def sidebar_dev_controls():
    st.sidebar.header("Developer Controls")

    st.sidebar.checkbox(
        "Show detailed outputs and logs",
        key="developer_view",
        value=False
    )


def build_sidebar_new(aadt_limit_table: pl.DataFrame, *, include_years=True):
    logger.info("[Sidebar] Building")

    init_intersection_config()
    sync_selected_with_intersection()
    init_aadt_limits(aadt_limit_table)
    sidebar_traffic_inputs()
    set_minor_aadt()

    if include_years:
        sidebar_years()

    sidebar_direct_estimation()
    sidebar_treatments()
    sidebar_dev_controls()


def show_session_state() -> None:
    """
    Just shows an alphabetized version of the session state values.
    """
    session_state_sorted = dict(sorted(st.session_state.items()))
    st.write(session_state_sorted)

# Resetting parameters code
# st.selectbox('Select:',['Please Select',1,2,3],key='selection')

# def reset():
#     st.session_state.selection = 'Please Select'

# st.button('Reset', on_click=reset)