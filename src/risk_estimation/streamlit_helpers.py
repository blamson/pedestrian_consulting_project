import streamlit as st
import polars as pl
from dataclasses import dataclass
from typing import Dict, Tuple
from loguru import logger
import re
import streamlit as st

# General helpers
@st.cache_data
def load_data(path: str) -> pl.DataFrame:
    """
    Load a CSV file into a Polars DataFrame (cached).

    Args:
        path (str): Filepath to the CSV file.

    Returns:
        pl.DataFrame: Loaded dataset as a Polars DataFrame.
    """
    return pl.read_csv(path)


@st.cache_data
def load_text(path: str) -> str:
    """
    Load a plain text file (cached).

    Typically used for UI help text tooltips and sidebar descriptions.

    Args:
        path (str): Filepath to text file.

    Returns:
        str: Raw text contents of the file.
    """
    with open(path) as f:
        return f.read()

# Classes
class Intersection:
    """
    Encapsulates intersection-specific configuration and derived parameters.

    This class acts as a deterministic configuration object that defines:
    - Intersection type-specific defaults
    - AADT constraints (major/minor road limits)
    - Behavioral flags for UI and model toggles
    - Helper methods for derived traffic quantities

    The configuration is selected based on a named intersection and
    internally maps to predefined structural assumptions.

    Attributes:
        name (str): User-selected intersection name.
        int_type (str): Primary intersection classification.
        int_type_alt (str | None): Optional alternate classification.
        minor_road (str): Label for minor roadway.
        minor_pct_default (float): Default minor road percentage.
        minor_pct_alt (float): Alternate minor road percentage.
        bulbout_default (bool): Default bulbout treatment state.
        signal_default (bool): Default signal presence.
        disable_minor_volume (bool): Whether minor volume input is locked.
        disable_direct_estimation (bool): Whether direct estimation inputs are disabled.
        pedvol_default (float): Default pedestrian volume.
        nlanes_default (int): Default number of lanes.

        max_aadt_major (int): Maximum allowed major road AADT.
        max_aadt_minor (int): Maximum allowed minor road AADT.
        max_aadt_major_alt (int | None): Alternate max major AADT.
        max_aadt_minor_alt (int | None): Alternate max minor AADT.
    """
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
        """
        Return the maximum allowable major road AADT for this intersection.

        If an alternate intersection type exists, returns the maximum across
        both primary and alternate configurations.

        Returns:
            int: Maximum supported major road AADT.
        """
        if self.max_aadt_major_alt:
            return max(self.max_aadt_major, self.max_aadt_major_alt)
        return self.max_aadt_major

    def compute_minor_aadt(self, aadt_major: int, pct: float) -> float:
        """
        Compute minor road AADT from major road AADT and turning percentage.

        Args:
            aadt_major (int): Major road traffic volume.
            pct (float): Minor road percentage (0–100 scale).

        Returns:
            float: Estimated minor road AADT, rounded to 2 decimals.
        """
        return round(aadt_major * pct / 100, 2)


@dataclass
class IntersectionInputs:
    """
    Container for all user-defined model inputs derived from the sidebar.

    Attributes:
        aadt_major (int): Major road traffic volume.
        minor_pct (float): Minor road percentage.
        years (int | None): Analysis horizon in years.
        pedvol (int): Pedestrian volume.
        nlanes (int): Number of lanes.
        cmf (Dict[str, bool]): Treatment flags (CMFs).
        developer_view (bool): Toggle for debug outputs.
    """
    aadt_major: int
    minor_pct: float
    years: int | None
    pedvol: int
    nlanes: int
    cmf: Dict[str, bool]
    developer_view: bool


# Sidebar components
def get_intersection(aadt_limit_table: pl.DataFrame) -> Intersection:
    """
    Create an Intersection object from user selection in the sidebar.

    This function binds UI selection state to a structured configuration
    object containing default parameters and constraints.

    Args:
        aadt_limit_table (pl.DataFrame): Lookup table defining AADT limits
            by intersection type.

    Returns:
        Intersection: Configured intersection instance.
    """

    st.sidebar.header("Intersection")

    name = st.sidebar.selectbox(
        "Please select an intersection",
        ("Agate & Mesa", "Agate & 4th"),
        key="intersection"
    )

    return Intersection(name, aadt_limit_table)


def sidebar_traffic_inputs(ixn: Intersection) -> Tuple[int, float, float]:
    """
    Collect traffic-related inputs from the Streamlit sidebar.

    Captures major road AADT, minor road percentage, and computes
    derived minor AADT. Also enforces model constraints on allowable
    traffic volumes.

    Args:
        ixn (Intersection): Active intersection configuration.

    Returns:
        Tuple[int, float, float]:
            - Major road AADT
            - Minor road percentage
            - Computed minor road AADT
    """
    st.sidebar.header("Traffic Parameters")

    aadt_major = st.sidebar.number_input(
        "Agate Traffic Volume",
        min_value=1,
        max_value=ixn.max_major(),
        step=5000,
        value=11000,
        key=f"{ixn.name}_aadt_major_selected",
        help=load_text("app_pages/text_files/help_text/aadt_major.txt"),
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
        help=load_text("app_pages/text_files/help_text/minor_percent.txt"),
    )

    aadt_minor = ixn.compute_minor_aadt(aadt_major, minor_pct)

    if aadt_minor > ixn.max_aadt_minor:
        st.sidebar.warning(
            f"Minor road volume exceeds limit of {ixn.max_aadt_minor}"
        )

    st.sidebar.metric(
        label=f"{ixn.minor_road} Traffic Volume",
        value=f"{int(aadt_minor)} veh/day",
        border=True
    )

    return aadt_major, minor_pct, aadt_minor


def sidebar_years() -> int:
    """
    Capture analysis duration from sidebar input.

    Returns:
        int: Number of years for long term risk estimation.
    """
    st.sidebar.header("Time Parameters")

    return st.sidebar.number_input(
        "Years",
        min_value=1,
        max_value=100,
        value=10,
        key="years",
        help=load_text("app_pages/text_files/help_text/years.txt"),
    )


def sidebar_direct_estimation(ixn: Intersection) -> Tuple[int, int]:
    """
    Collect direct estimation inputs (pedestrians and lanes).

    These inputs are used in signalized pestrian models. 

    Args:
        ixn (Intersection): Active intersection configuration.

    Returns:
        Tuple[int, int]:
            - Pedestrian volume
            - Number of lanes
    """
    st.sidebar.header("Direct Estimation Parameters")

    pedvol = st.sidebar.number_input(
        "Daily Pedestrian Volume",
        min_value=1,
        max_value=1000,
        step=100,
        value=int(ixn.pedvol_default),
        key=f"{ixn.name}_pedvol_selected",
        disabled=ixn.disable_direct_estimation,
        help=load_text("app_pages/text_files/help_text/pedvol.txt"),
    )

    nlanes = st.sidebar.number_input(
        "Number of Lanes",
        min_value=1,
        max_value=10,
        step=1,
        value=ixn.nlanes_default,
        key=f"{ixn.name}_nlanes_selected",
        disabled=ixn.disable_direct_estimation,
        help=load_text("app_pages/text_files/help_text/nlanes.txt"),
    )

    return pedvol, nlanes


def sidebar_treatments(ixn: Intersection) -> Dict[str, bool]:
    """
    Collect CMF boolean flags from the sidebar.

    Each boolean corresponds to an active safety or design treatment
    used in downstream crash modification factor calculations.

    Args:
        ixn (Intersection): Active intersection configuration.

    Returns:
        Dict[str, bool]: Mapping of CMF names to activation state.
    """
    st.sidebar.header("Intersection Treatments")

    twltl = st.sidebar.checkbox(
        "Two Way Left Turn Lane",
        value=True,
        key=f"{ixn.name}_twltl_cmf",
        help=load_text("app_pages/text_files/help_text/twltl.txt")
    )

    lighting = st.sidebar.checkbox(
        "Street Lights",
        value=True,
        key=f"{ixn.name}_lighting_cmf",
        help=load_text("app_pages/text_files/help_text/street_lights.txt")
    )

    bulbout = st.sidebar.checkbox(
        "Bulbout",
        value=ixn.bulbout_default,
        key=f"{ixn.name}_bulbout_cmf",
        help=load_text("app_pages/text_files/help_text/bulbout.txt")
    )

    signal = st.sidebar.checkbox(
        "Traffic Signal",
        value=ixn.signal_default,
        key=f"{ixn.name}_signal_cmf",
        disabled=(ixn.int_type != "4st"),
        help=load_text("app_pages/text_files/help_text/traffic_signal.txt")
    )

    return {
        "twltl_cmf": twltl,
        "lighting_cmf": lighting,
        "bulbout_cmf": bulbout,
        "signal_cmf": signal if ixn.int_type == "4st" else False,
    }


def sidebar_dev_controls() -> bool:
    """
    Toggle developer/debug mode in the UI.

    Returns:
        bool: True if developer outputs should be shown.
    """
    st.sidebar.header("Developer Controls")

    return st.sidebar.checkbox(
        "Show debug information",
        value=False,
        key="developer_view",
    )

# Full sidebar creation
def build_sidebar(
    aadt_limit_table: pl.DataFrame,
    *,
    include_years: bool = True
) -> tuple[Intersection, IntersectionInputs]:
    """
    Construct full sidebar UI and return structured inputs.

    This function orchestrates all sidebar components and converts
    Streamlit state into a structured model input object.

    Workflow:
        1. Select intersection configuration
        2. Capture traffic inputs
        3. Optionally capture time horizon
        4. Capture direct estimation parameters
        5. Capture CMF treatment flags
        6. Capture developer settings

    Args:
        aadt_limit_table (pl.DataFrame): Lookup table for AADT constraints.
        include_years (bool): Whether to include time horizon input.

    Returns:
        tuple:
            Intersection: Configured intersection object.
            IntersectionInputs: Aggregated model input object.
    """

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


def show_debug(ixn: Intersection, inputs: IntersectionInputs):
    """
    Render developer/debug information in Streamlit.

    Displays raw object state for inspection of:
    - Intersection configuration
    - User input aggregation

    Args:
        ixn (Intersection): Intersection configuration object.
        inputs (IntersectionInputs): Aggregated sidebar inputs.

    Returns:
        None
    """
    dev_container = st.container(border=True, height=300)
    dev_container.header("BEBUG INFORMATION")
    dev_container.header("Intersection class information")
    dev_container.write(ixn)
    dev_container.header("Input class information")
    dev_container.write(inputs)
    dev_container.header("Streamlit Session State")
    dev_container.write(st.session_state)


# def render_report_page(md_filename: str, project_root: Path) -> None:
#     """
#     Render a markdown report file with inline images in Streamlit.
#     Parses standard markdown image syntax and renders images via st.image:
#     - Splits markdown around ![alt](path) markers
#     - Resolves image paths relative to the project root
#     - Supports an optional width hint via |WIDTH in the alt text
#     Args:
#         md_filename (str): Filename of the markdown file in docs/report_sections/.
#         project_root (Path): Absolute path to the project root directory.
#     Returns:
#         None
#     """
#     md_path = project_root / "docs/report_sections" / md_filename
#     content = md_path.read_text()
#     parts = re.split(r'!\[([^\]]*)\]\(([^)]+)\)', content)

#     i = 0
#     while i < len(parts):
#         if parts[i].strip():
#             st.markdown(parts[i])
#         if i + 2 < len(parts):
#             alt_raw, img_path = parts[i+1], parts[i+2]
#             width = None
#             alt = alt_raw
#             if '|' in alt_raw:
#                 left, right = alt_raw.rsplit('|', 1)
#                 try:
#                     width = int(right.strip())
#                     alt = left
#                 except ValueError:
#                     pass
#             full_img = project_root / img_path
#             if full_img.exists():
#                 kwargs = {"caption": alt or None}
#                 if width:
#                     kwargs["width"] = width
#                 st.image(str(full_img), **kwargs)
#             else:
#                 st.error(f"Image not found: {full_img}")
#             i += 3
#         else:
#             i += 1

def render_report_page(md_filename: str, project_root: Path) -> None:
    """
    Render a markdown report file with inline images in Streamlit.
    Supports standard markdown image syntax with optional width hints, and
    image rows wrapped in HTML comment markers:
    - ![caption|450](path) renders at 450px width
    - Images between <!-- row --> and <!-- /row --> render side-by-side
    Args:
        md_filename (str): Filename of the markdown file in docs/report_sections/.
        project_root (Path): Absolute path to the project root directory.
    Returns:
        None
    """
    md_path = project_root / "docs/report_sections" / md_filename
    content = md_path.read_text()

    row_pattern = r'<!--\s*row\s*-->(.*?)<!--\s*/row\s*-->'
    cursor = 0
    for match in re.finditer(row_pattern, content, re.DOTALL):
        _render_chunk(content[cursor:match.start()], project_root)
        _render_image_row(match.group(1), project_root)
        cursor = match.end()
    _render_chunk(content[cursor:], project_root)


def _render_chunk(text: str, project_root: Path) -> None:
    parts = re.split(r'!\[([^\]]*)\]\(([^)]+)\)', text)
    i = 0
    while i < len(parts):
        if parts[i].strip():
            st.markdown(parts[i])
        if i + 2 < len(parts):
            alt_raw, img_path = parts[i+1], parts[i+2]
            width = None
            alt = alt_raw
            if '|' in alt_raw:
                left, right = alt_raw.rsplit('|', 1)
                try:
                    width = int(right.strip())
                    alt = left
                except ValueError:
                    pass
            full_img = project_root / img_path
            if not full_img.exists():
                st.error(f"Image not found: {full_img}")
                i += 3
                continue
            if width:
                # Constrain via columns so image renders at native resolution
                # Assumes ~1100px content width under wide layout
                ratio = min(max(width / 1100, 0.2), 1.0)
                if ratio < 1.0:
                    pad = (1 - ratio) / 2
                    cols = st.columns([pad, ratio, pad])
                    with cols[1]:
                        st.image(str(full_img), caption=alt or None, use_container_width=True)
                else:
                    st.image(str(full_img), caption=alt or None, use_container_width=True)
            else:
                st.image(str(full_img), caption=alt or None)
            i += 3
        else:
            i += 1


def _render_image_row(row_content: str, project_root: Path) -> None:
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', row_content)
    if not images:
        return
    cols = st.columns(len(images))
    for col, (alt_raw, img_path) in zip(cols, images):
        alt = alt_raw.rsplit('|', 1)[0] if '|' in alt_raw else alt_raw
        full_img = project_root / img_path
        with col:
            if full_img.exists():
                st.image(str(full_img), caption=alt or None, use_container_width=True)
            else:
                st.error(f"Image not found: {full_img}")