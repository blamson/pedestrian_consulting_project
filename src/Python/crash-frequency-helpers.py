import polars as pl
import math
from math import exp, log, prod
from scipy.stats import poisson


def is_missing_like(x) -> bool:
    # None
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
    if is_missing_like(value):
        raise ValueError(f"{variable_name} is missing or invalid")


def validate_inputs(
  int_type: str, 
  aadt_major: int, 
  aadt_minor: int, 
  aadt_max: int,
  signal_cmf: bool,
  pedvol = None, 
  nlanes = None
) -> None:
    print(int_type)


def compute_vehicle_spf(
    spf_row: pl.DataFrame, 
    aadt_major: int, 
    aadt_minor: int
) -> float: 

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
    Source: HSM formula 12-29

    Args:
        spf_row: A single row of a polars dataframe containing the coefficients a through e
        aadt_major: Major road AADT
        aadt_minor: Minor road AADT
        pedvol: Daily pedestrian volume
        nlanes: Maximum number of lanes crossed by pedestrians

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

        calc_ped_cmf: Dictates which set of cmfs can even be considered

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
        int_type: 4st or 3st

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
        num_accidents_per_year: Expected accidents per year. Must be positive.
        years: Integer number of years, must be at least 1. 

    Returns:
        Probability of at least one accident in t years

    Raises:
        ValueError when improper values of either argument are provided
    """

    if num_accidents_per_year <= 0:
        raise ValueError(f"Expected accidents must be a positive value. Provided: {num_accidents_per_year}")

    if years <= 1:
        raise ValueError(f"Years must be a positive value at least 1. Provided: {years}")

    theta = num_accidents_per_year * years
    return 1 - poisson.pmf(0, theta)


def estimate_crashes(
    spfs: pl.DataFrame,
    int_name,
    int_type,
    aadt_major,
    aadt_minor,
    aadt_max = None,
    years = 10,
    # Signalized only variables ---
    pedvol=None,
    nlanes=None,
    # CMFs ---
    lighting_cmf=True,
    twltl_cmf=True,
    signal_cmf=False,
    # Pedestrian only CMFs ---
    bulbout_cmf=False,
    school_cmf=False # pedestrian and signalized only
) -> dict:

    int_type = "".join(int_type.split()).lower()

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
        "lighting": lighting_cmf,
        "twltl": twltl_cmf,
        "bulbout": bulbout_cmf,
        "signal_cmf": signal_cmf,
        "school": school_cmf,
        "pedvol": pedvol,
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


spfs = pl.read_csv("data/spfs.csv")
x = estimate_crashes(spfs=spfs, int_name="Agate & 4th", int_type="4st", aadt_major=11000, aadt_minor=836)
for key, value in x.items():
    print(key, value)