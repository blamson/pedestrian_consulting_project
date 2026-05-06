import streamlit as st
import polars as pl
from dataclasses import dataclass
from typing import Dict, Tuple
from loguru import logger


# =========================
# Data Loading
# =========================

@st.cache_data
def load_data(path: str) -> pl.DataFrame:
    return pl.read_csv(path)


@st.cache_data
def load_text(path: str) -> str:
    with open(path) as f:
        return f.read()


# =========================
# Domain Model
# =========================

class Intersection:
    def __init__(self, name: str, aadt_limit_table: pl.DataFrame):
        self.name = name

        if name == "Agate & Mesa":
            self.int_type = "3st"
            self.int_type_alt = None
            self.minor_road = "Mesa"
            self.minor_pct_default = 3.2
            self.minor_pct_alt = 16.6
            self.bulbout_default = True
            self.signal_default = False
            self.disable_minor_volume = False
            self.disable_direct_estimation = True
            self.pedvol_default = 138.4
            self.nlanes_default = 5

        else:
            self.int_type = "4st"
            self.int_type_alt = "4sg"
            self.minor_road = "4th"
            self.minor_pct_default = 7.6
            self.minor_pct_alt = 12.6
            self.bulbout_default = False
            self.signal_default = True
            self.disable_minor_volume = True
            self.disable_direct_estimation = False
            self.pedvol_default = 145.32
            self.nlanes_default = 5

        # --- AADT limits ---
        df_default = aadt_limit_table.filter(
            pl.col("intersection_type") == self.int_type
        )

        self.max_aadt_major = df_default["aadt_major"].item()
        self.max_aadt_minor = df_default["aadt_minor"].item()

        self.max_aadt_major_alt = None
        self.max_aadt_minor_alt = None

        if self.int_type_alt:
            df_alt = aadt_limit_table.filter(
                pl.col("intersection_type") == self.int_type_alt
            )
            if not df_alt.is_empty():
                self.max_aadt_major_alt = df_alt["aadt_major"].item()
                self.max_aadt_minor_alt = df_alt["aadt_minor"].item()

    def max_major(self) -> int:
        if self.max_aadt_major_alt:
            return max(self.max_aadt_major, self.max_aadt_major_alt)
        return self.max_aadt_major

    def compute_minor_aadt(self, aadt_major: int, pct: float) -> float:
        return round(aadt_major * pct / 100, 2)


# =========================
# Inputs Container
# =========================

@dataclass
class IntersectionInputs:
    aadt_major: int
    minor_pct: float
    years: int | None
    pedvol: int
    nlanes: int
    cmf: Dict[str, bool]
    developer_view: bool


# =========================
# Sidebar Components
# =========================

def get_intersection(aadt_limit_table: pl.DataFrame) -> Intersection:
    st.sidebar.header("Intersection")

    name = st.sidebar.selectbox(
        "Please select an intersection",
        ("Agate & Mesa", "Agate & 4th"),
        key="intersection"
    )

    return Intersection(name, aadt_limit_table)


def sidebar_traffic_inputs(ixn: Intersection) -> Tuple[int, float, float]:
    st.sidebar.header("Traffic Parameters")

    aadt_major = st.sidebar.number_input(
        "Agate Traffic Volume",
        min_value=1,
        max_value=ixn.max_major(),
        step=5000,
        value=11000,
        key=f"{ixn.name}_aadt_major_selected",
        help=load_text("pages/text_files/help_text/aadt_major.txt"),
    )

    minor_pct = st.sidebar.number_input(
        f"{ixn.minor_road} Traffic Percent",
        min_value=0.01,
        max_value=99.0,
        step=5.0,
        value=ixn.minor_pct_default,
        key=f"{ixn.name}_minor_pct_selected",
        format="%.1f",
        disabled=ixn.disable_minor_volume,
        help=load_text("pages/text_files/help_text/minor_percent.txt"),
    )

    aadt_minor = ixn.compute_minor_aadt(aadt_major, minor_pct)

    if aadt_minor > ixn.max_aadt_minor:
        st.sidebar.warning(
            f"Minor road volume exceeds limit of {ixn.max_aadt_minor}"
        )

    st.sidebar.metric(
        label=f"{ixn.minor_road} Traffic Volume",
        value=f"{int(aadt_minor)} veh/day"
    )

    return aadt_major, minor_pct, aadt_minor


def sidebar_years() -> int:
    st.sidebar.header("Time Parameters")

    return st.sidebar.number_input(
        "Years",
        min_value=1,
        max_value=100,
        value=10,
        key="years",
        help=load_text("pages/text_files/help_text/years.txt"),
    )


def sidebar_direct_estimation(ixn: Intersection) -> Tuple[int, int]:
    st.sidebar.header("Direct Estimation Parameters")

    pedvol = st.sidebar.number_input(
        "Daily Pedestrian Volume",
        min_value=1,
        max_value=1000,
        step=100,
        value=int(ixn.pedvol_default),
        key=f"{ixn.name}_pedvol_selected",
        disabled=ixn.disable_direct_estimation,
        help=load_text("pages/text_files/help_text/pedvol.txt"),
    )

    nlanes = st.sidebar.number_input(
        "Number of Lanes",
        min_value=1,
        max_value=10,
        step=1,
        value=ixn.nlanes_default,
        key=f"{ixn.name}_nlanes_selected",
        disabled=ixn.disable_direct_estimation,
        help=load_text("pages/text_files/help_text/nlanes.txt"),
    )

    return pedvol, nlanes


def sidebar_treatments(ixn: Intersection) -> Dict[str, bool]:
    st.sidebar.header("Intersection Treatments")

    twltl = st.sidebar.checkbox(
        "Two Way Left Turn Lane",
        value=True,
        key=f"{ixn.name}_twltl_cmf",
    )

    lighting = st.sidebar.checkbox(
        "Street Lights",
        value=True,
        key=f"{ixn.name}_lighting_cmf",
    )

    bulbout = st.sidebar.checkbox(
        "Bulbout",
        value=ixn.bulbout_default,
        key=f"{ixn.name}_bulbout_cmf",
    )

    signal = st.sidebar.checkbox(
        "Traffic Signal",
        value=ixn.signal_default,
        key=f"{ixn.name}_signal_cmf",
        disabled=(ixn.int_type != "4st"),
    )

    return {
        "twltl_cmf": twltl,
        "lighting_cmf": lighting,
        "bulbout_cmf": bulbout,
        "signal_cmf": signal if ixn.int_type == "4st" else False,
    }


def sidebar_dev_controls() -> bool:
    st.sidebar.header("Developer Controls")

    return st.sidebar.checkbox(
        "Show detailed outputs and logs",
        value=False,
        key="developer_view",
    )


# =========================
# Sidebar Builder (FINAL)
# =========================

def build_sidebar_new(
    aadt_limit_table: pl.DataFrame,
    *,
    include_years: bool = True
) -> tuple[Intersection, IntersectionInputs]:

    logger.info("[Sidebar] Building")

    ixn = get_intersection(aadt_limit_table)

    aadt_major, minor_pct, _ = sidebar_traffic_inputs(ixn)

    years = sidebar_years() if include_years else None

    pedvol, nlanes = sidebar_direct_estimation(ixn)

    cmf = sidebar_treatments(ixn)

    developer_view = sidebar_dev_controls()

    inputs = IntersectionInputs(
        aadt_major=aadt_major,
        minor_pct=minor_pct,
        years=years,
        pedvol=pedvol,
        nlanes=nlanes,
        cmf=cmf,
        developer_view=developer_view,
    )

    return ixn, inputs


# =========================
# Debug Helper
# =========================

def show_debug(ixn: Intersection, inputs: IntersectionInputs):
    st.write("### Intersection Config")
    st.write(ixn.__dict__)

    st.write("### Inputs")
    st.write(inputs)