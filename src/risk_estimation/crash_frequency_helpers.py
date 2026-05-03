import polars as pl
import math
from math import exp, log, prod
import numpy as np
from scipy.stats import poisson
from loguru import logger


def is_missing_like(x) -> bool:
    """
    Determine whether an input should be treated as "missing-like".

    This function generalizes missingness across several input types:
    - None
    - NaN (scalar float)
    - Empty iterables (list, tuple)
    - Iterables containing only None or NaN
    - Polars Series that are empty or entirely null/NaN

    Args:
        x: Input value to evaluate.

    Returns:
        bool: True if the input is considered missing-like, False otherwise.
    """
    if x is None:
        return True

    # Polars Series
    if isinstance(x, pl.Series):
        if x.len() == 0:
            return True
        return x.is_null().all() or x.is_nan().all()

    # Python iterables (lists, tuples)
    if isinstance(x, (list, tuple)):
        if len(x) == 0:
            return True
        return all(
            (v is None) or (isinstance(v, float) and math.isnan(v))
            for v in x
        )

    # Scalar NaN
    if isinstance(x, float) and math.isnan(x):
        return True

    return False


def stop_if_missing_like(variable_name, value) -> None:
    """
    Raise an error if a value is considered "missing-like".

    This is a guard function that wraps `is_missing_like` and provides
    a standardized error message for invalid inputs.

    Args:
        variable_name (str): Name of the variable being validated.
        value: Value to check.

    Raises:
        ValueError: If `value` is missing-like.
    """
    if is_missing_like(value):
        raise ValueError(f"{variable_name} is missing or invalid")


def validate_inputs(
  int_type: str, 
  aadt_major: int, 
  aadt_minor: int, 
  aadt_max: int,
  signal_cmf: bool,
  pedvol = None, 
  nlanes = None,
  scenario="Not Specified"
) -> None:
    """
    Validate inputs for intersection crash prediction models.

    Performs consistency and domain checks across:
    - Required inputs (non-missing)
    - Supported intersection types
    - Signalized intersection constraints
    - AADT ordering and upper bounds

    Args:
        int_type (str): Intersection type identifier (must exist in `aadt_max`).
        aadt_major (int): Major road AADT; must be positive and within limits.
        aadt_minor (int): Minor road AADT; must be positive, <= major, and within limits.
        aadt_max (pl.DataFrame): Lookup table containing maximum allowable AADT
            values by intersection type. Must contain columns:
            ["intersection_type", "aadt_major", "aadt_minor"].
        signal_cmf (bool): Whether a signal CMF is applied.
        pedvol (int, optional): Pedestrian volume (required for signalized SPFs).
        nlanes (int, optional): Number of lanes (required for signalized SPFs).

    Raises:
        ValueError:
            - If required inputs are missing-like
            - If `int_type` is unsupported
            - If signalized SPF constraints are violated
            - If AADT values are non-positive, misordered, or exceed limits
            - If `aadt_max` does not contain exactly one row for `int_type`
        Warning:
            - If AADT values exceed their model specific limits

    Returns:
        None
    """
    
    logger.info(f"Validating inputs for scenario <{scenario}>...")
    # Existence checks
    stop_if_missing_like("int_type", int_type)
    stop_if_missing_like("aadt_major", aadt_major)
    stop_if_missing_like("aadt_minor", aadt_minor)
    stop_if_missing_like("aadt_max", aadt_max)

    available_int_types = set(aadt_max["intersection_type"].to_list())
    if int_type not in available_int_types:
        raise ValueError(f"Unsupported intersection type: {int_type}")
    
    # Signalized SPF checks
    if int_type in ["3sg", "4sg"]:
        stop_if_missing_like("pedvol", pedvol)
        stop_if_missing_like("nlanes", nlanes)
        if signal_cmf:
            raise ValueError("signal_cmf cannot be applied when using a signalized spf")

        if nlanes <= 0:
            raise ValueError(f"nlanes must be a positive value: {nlanes}")
        if pedvol <= 0:
            raise ValueError(f"pedvol must be a positive value: {pedvol}")

    # AADT Checks
    if aadt_minor <= 0 or aadt_major <= 0:
        raise ValueError(f"AADT variables must be positive values. aadt_minor: {aadt_minor}, aadt_major: {aadt_major}")

    aadt_limits = aadt_max.filter(pl.col("intersection_type") == int_type)
    limit_rows = aadt_limits.height
    if limit_rows != 1:
        raise ValueError(f"Expected exactly one row for {int_type} in aadt_max dataset") 
    
    if aadt_minor > aadt_major:
        raise ValueError(f"aadt_minor exceeds aadt_major: {aadt_minor} > {aadt_major}")
    
    major_limit = aadt_limits["aadt_major"].item()
    minor_limit = aadt_limits["aadt_minor"].item()

    if aadt_major > major_limit:
        logger.warning(f"aadt_major exceeds model specific limit for {int_type}: {aadt_major} > {major_limit}")
    
    if aadt_minor > minor_limit:
        logger.warning(f"aadt_minor exceeds model specific limit for {int_type}: {aadt_minor} > {minor_limit}")

    logger.success("All checks passed")
    return None


def compute_vehicle_spf(
    spf_row: pl.DataFrame, 
    aadt_major: int, 
    aadt_minor: int
) -> float: 
    """
    Computes the base expected frequency of a given crash type for vehicles.
    This SPF is used for stop controlled intersections.
    Sources:
        HSM equations 12-21 and 12-24

    Args:
        `spf_row`: A single row of a polars dataframe containing the coefficients a through c
        `aadt_major`: Major road AADT
        `aadt_minor`: Minor road AADT

    Returns:
        float: Expected number of vehicle crashes per year
    """

    return exp(
        spf_row["a"].item() +
        spf_row["b"].item() * log(aadt_major) +
        spf_row["c"].item() * log(aadt_minor)
    )


def compute_signalized_pedestrian_spf(
    spf_row: pl.DataFrame, 
    aadt_major: int, 
    aadt_minor: int,
    pedvol: float,
    nlanes: int
) -> float: 
    """
    Computes the base expected crash frequency per year for pedestrians.
    This SPF only works for signalized intersections as those are the only ones with the necessary coefficients. 
    
    Sources: 
        HSM equation 12-29
        SPFs commonly used taken from HSM table 12-14

    Args:
        `spf_row`: A single row of a polars dataframe containing the coefficients a through e
        `aadt_major`: Major road AADT
        `aadt_minor`: Minor road AADT
        `pedvol`: Daily pedestrian volume
        `nlanes`: Maximum number of lanes crossed by pedestrians

    Returns:
        float: Expected number of pedestrian crashes per year
    """

    return exp(
        spf_row["a"].item() +
        spf_row["b"].item() * log(aadt_major + aadt_minor) +
        spf_row["c"].item() * log(aadt_minor / aadt_major) +
        spf_row["d"].item() * log(pedvol) +
        spf_row["e"].item() * nlanes
    )


def compute_cmfs(
    lighting_cmf: bool = False,
    twltl_cmf: bool = False,
    signal_cmf: bool = False,
    bulbout_cmf: bool = False,
    school_cmf: bool = False,
    calc_ped_cmf: bool = False
) -> float:
    """
    Calculates the overall CMF value relevant to all crash types.
    The specific hard-coded values are taken either from the HSM or cmfclearinghouse.

    Sources:
        Lighting: HSM equation 12-36
        Two Way Left Turn Lane: cmfclearinghouse - cmid 1285
        Traffic Signal: cmfclearinghouse - cmid319
        Bulbout: cmfclearinghouse - cmid 1786
        School: HSM table 12-29

    Args: 
        All cmf arguments are booleans that dictate if a given cmf should be applied.
        Note that the signal cmf should not be applied when a signalized spf is being used.
        lighting, twltl and signal are ALL CRASH cmfs
        bulbout and school are PEDESTRIAN cmfs

        `calc_ped_cmf`: Dictates which set of cmfs can even be considered

    Returns:
        float: Product of all cmf values for given set of accident types
    """

    if calc_ped_cmf:
        factors = {
            "bulbout": 0.63 if bulbout_cmf else 1,
            "school": 1.35 if school_cmf else 1
        }

    else:
        factors = {
            "lighting": 0.91 if lighting_cmf else 1,
            "twltl": 0.92 if twltl_cmf else 1,
            "signal_cmf": 0.77 if signal_cmf else 1
        }

    return prod(factors.values())


def get_pedestrian_factor(
    int_type: str
) -> float:
    """
    For stop controlled intersections, pedestrian crashes are estimated as a flat proportion
    of the overall crash frequency. 
    This proportion varies between 3 and 4 way intersections.

    Sources: 
        HSM Table 12-16

    Args:
        `int_type`: 4st or 3st

    Returns: 
        Pedestrian crash adjustment factor for stop controlled intersections.

    Raises:
        Value Error if the right type of intersection isn't provided. 
    """

    match int_type:
        case "3st":
            return 0.021
        case "4st":
            return 0.022
        case _:
            raise ValueError(f"Pedestrian factors may only be provided for stop controlled intersections. int_type provided: {int_type}")
        

def calc_long_run_accident_probability(
    num_accidents_per_year: float = 1,
    years: int = 10
) -> float:
    """
    Returns the probability of at least one accident in a 't' year period
    This function leverages the Poisson pdf by setting the expected crash frequency to lambda.
    The number of years simply scales lambda up if increased above 1.

    Probability Statement:
        1 - P(0 accidents in 't' years)
        where theta = num_accidents_per_year * years
    
    Args:
        `num_accidents_per_year`: Expected accidents per year. Must be positive.
        `years`: Integer number of years, must be at least 1. 

    Returns:
        Probability of at least one accident in t years

    Raises:
        ValueError when improper values of either argument are provided
    """

    if num_accidents_per_year <= 0:
        raise ValueError(f"Expected accidents must be a positive value. Provided: {num_accidents_per_year}")

    if years < 1:
        raise ValueError(f"Years must be a positive value of at least 1. Provided: {years}")

    theta = num_accidents_per_year * years
    return 1 - poisson.pmf(0, theta)


def estimate_crashes(
    spfs: pl.DataFrame,
    int_name,
    int_type,
    aadt_major,
    aadt_minor,
    scenario_name="baseline",
    aadt_max = None,
    years = 10,
    pedvol=None,
    nlanes=None,
    lighting_cmf=True,
    twltl_cmf=True,
    signal_cmf=False,
    bulbout_cmf=False,
    school_cmf=False
) -> dict:
    """
    Estimate expected vehicle and pedestrian crashes for an intersection.

    This function applies Safety Performance Functions (SPFs) and Crash
    Modification Factors (CMFs) to compute:
    - Baseline multi-vehicle and single-vehicle crash frequencies
    - Pedestrian crash frequency (via SPF or proportional factor)
    - Adjusted crash predictions under selected CMFs
    - Long-run probability of at least one pedestrian crash over a time horizon

    Workflow:
    1. Validate inputs and normalize `int_type`.
    2. Subset SPF data by intersection and crash type.
    3. Compute baseline vehicle crashes (multi-vehicle + single-vehicle).
    4. Compute baseline pedestrian crashes:
       - Signalized intersections: SPF-based
       - Unsignalized intersections: proportional to total vehicle crashes
    5. Apply CMFs to adjust vehicle and pedestrian predictions.
    6. Compute long-run pedestrian crash probability over `years`.

    Args:
        `spfs` (pl.DataFrame): SPF dataset containing at minimum:
            ["intersection_type", "crash_type", ... model parameters ...].
        `int_name` (str): Identifier for the intersection.
        `int_type` (str): Intersection type (case/whitespace insensitive).
        `aadt_major` (int): Major road AADT.
        `aadt_minor` (int): Minor road AADT.
        `aadt_max` (pl.DataFrame, optional): Lookup table of maximum allowable
            AADT values by intersection type.
        `years` (int, default=10): Time horizon for probability calculation.
        `pedvol` (int, optional): Pedestrian volume (required for signalized SPFs).
        `nlanes` (int, optional): Number of lanes (required for signalized SPFs).
        `lighting_cmf` (bool, default=True): Apply lighting CMF.
        `twltl_cmf` (bool, default=True): Apply two-way left-turn lane CMF.
        `signal_cmf` (bool, default=False): Apply signal CMF (unsignalized only).
        `bulbout_cmf` (bool, default=False): Apply bulb-out CMF (pedestrian).
        `school_cmf` (bool, default=False): Apply school-zone CMF (pedestrian).

    Returns:
        dict: Dictionary of inputs, intermediate quantities, and outputs, including:
            - Baseline crashes: "nbi_mv", "nbi_sv", "nbi_all", "nped_base"
            - CMFs: "cmf_veh", "cmf_ped"
            - Predictions: "pred_veh", "pred_ped"
            - Long-run probability: "long_run_ped_prob"
            - Metadata and inputs

    Raises:
        ValueError: If input validation fails (see `validate_inputs`).

    Notes:
        - Pedestrian crash estimation differs structurally between signalized
          ("3sg", "4sg") and unsignalized intersection types.
        - CMFs are applied multiplicatively.
        - Long-run probability assumes a Poisson process with rate `pred_ped`.
    """

    int_type = "".join(int_type.split()).lower()

    validate_inputs(int_type, aadt_major, aadt_minor, aadt_max, signal_cmf, pedvol, nlanes, scenario=scenario_name)

    # Clean up int and crash columns to be easier to work with
    spfs = (
        spfs
        .with_columns(
            intersection_type = pl.col("intersection_type").str.to_lowercase(),
            crash_type = pl.col("crash_type").str.to_lowercase()
        )
    )

    spf_mv = (
        spfs
        .filter(
            (pl.col("intersection_type") == int_type) &
            (pl.col("crash_type") == "mv")
        )
    )

    spf_sv = (
        spfs
        .filter(
            (pl.col("intersection_type") == int_type) &
            (pl.col("crash_type") == "sv")
        )
    )

    # Calculate multi and single vehicle crash rates
    nbimv = compute_vehicle_spf(spf_mv, aadt_major, aadt_minor)
    nbisv = compute_vehicle_spf(spf_sv, aadt_major, aadt_minor)
    nbi = nbimv + nbisv

    # Pedestrian crash rates
    if int_type in ["4sg", "3sg"]:
        spf_ped = (
            spfs
            .filter(
                (pl.col("intersection_type") == int_type) &
                (pl.col("crash_type") == "ped")
            )
        )

        nped_base = compute_signalized_pedestrian_spf(spf_ped, aadt_major, aadt_minor, pedvol, nlanes)
        fpedi = None

    else:
        fpedi = get_pedestrian_factor(int_type)
        nped_base = nbi * fpedi
    
    cmf_veh = compute_cmfs(lighting_cmf=lighting_cmf, twltl_cmf=twltl_cmf, signal_cmf=signal_cmf)
    cmf_ped = compute_cmfs(bulbout_cmf=bulbout_cmf, school_cmf=school_cmf, calc_ped_cmf=True)

    pred_veh = nbi * cmf_veh
    pred_ped = nped_base * cmf_veh * cmf_ped
    long_run_prob = calc_long_run_accident_probability(num_accidents_per_year=pred_ped, years=years)

    return {
        "intersection_name": int_name,
        "intersection_type": int_type,
        "scenario": scenario_name,
        "lighting_cmf": lighting_cmf,
        "twltl_cmf": twltl_cmf,
        "bulbout_cmf": bulbout_cmf,
        "signal_cmf": signal_cmf,
        "school_cmf": school_cmf,
        "pedvol_cmf": pedvol,
        "nlanes": nlanes,
        "aadt_maj": aadt_major,
        "aadt_minor": aadt_minor,
        "nbi_mv": nbimv,
        "nbi_sv": nbisv,
        "nbi_all": nbi,
        "nped_base": nped_base,
        "cmf_veh": cmf_veh,
        "cmf_ped": cmf_ped,
        "ped_factor": fpedi,
        "pred_veh": pred_veh,
        "pred_ped": pred_ped,
        "long_run_ped_prob": long_run_prob,
        "years": years
    }


def sweep_aadt_major(
    spfs,
    int_name,
    int_type,
    aadt_max,
    aadt_major_min,
    aadt_major_max,
    k,
    years=10,
    steps=50,
    **fixed_inputs
) -> pl.DataFrame:

    aadt_major_grid = np.linspace(aadt_major_min, aadt_major_max, steps)

    rows = []
    aadt_limits = aadt_max.filter(pl.col("intersection_type") == int_type)
    for aadt_major in aadt_major_grid:
        aadt_minor = k * aadt_major
        if aadt_minor <= aadt_limits["aadt_minor"].item():
            result = estimate_crashes(
                spfs=spfs,
                int_name=int_name,
                int_type=int_type,
                aadt_major=float(aadt_major),
                aadt_minor=float(aadt_minor),
                aadt_max=aadt_max,
                years=years,
                **fixed_inputs
            )

            rows.append({
                "aadt_major": float(aadt_major),
                "aadt_minor": float(aadt_minor),
                "pred_ped": result["pred_ped"],
                f"{years}_year_crash_probability": result["long_run_ped_prob"]
            })

    return pl.DataFrame(rows)


def _to_list(x):
    if x is None:
        return None
    if isinstance(x, (list, tuple)):
        return list(x)
    if isinstance(x, range):
        return list(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    return [x]  # scalar fallback


def sweep_estimates(
    spfs: pl.DataFrame,
    int_name,
    int_type,
    aadt_major_vals,
    k_vals=None,
    years_vals=None,
    **kwargs
) -> pl.DataFrame:

    aadt_major_vals = _to_list(aadt_major_vals) or [kwargs.get("aadt_major")]
    k_vals = _to_list(k_vals) or [kwargs.get("k", 0.3)]
    years_vals = _to_list(years_vals) or [kwargs.get("years", 10)]

    # Build parameter grid
    grid = (
        pl.DataFrame({"aadt_major": aadt_major_vals})
        .join(pl.DataFrame({"k": k_vals}), how="cross")
        .join(pl.DataFrame({"years": years_vals}), how="cross")
        .with_columns(
            (pl.col("aadt_major") * pl.col("k")).alias("aadt_minor")
        )
    )

    rows = grid.to_dicts()

    results = [
        {
            **row,
            **estimate_crashes(
                spfs=spfs,
                int_name=int_name,
                int_type=int_type,
                aadt_major=row["aadt_major"],
                aadt_minor=row["aadt_minor"],
                years=row["years"],
                **kwargs
            )
        }
        for row in rows
    ]

    results = pl.DataFrame(results)
    return(results)
