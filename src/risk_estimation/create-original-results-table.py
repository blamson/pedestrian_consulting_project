import polars as pl
import json
from risk_estimation.streamlit_helpers import Intersection
from risk_estimation.crash_frequency_helpers import estimate_crashes
from loguru import logger
from datetime import datetime

aadt_limits = pl.read_csv("data/aadt_maximums.csv")
spfs = pl.read_csv("data/spfs.csv")
mesa = Intersection("Agate & Mesa", aadt_limits)
fourth = Intersection("Agate & 4th", aadt_limits)
print("---")
logger.info("Showing intersection objects")
int_vars = [vars(mesa), vars(fourth)]
[print(json.dumps(intersection, indent=4)) for intersection in int_vars]

scenarios = []
aadt_major = 11000
# Run through mesa scenarios ----
logger.info("CREATING MESA RESULTS")
before_low = estimate_crashes(
    spfs=spfs,
    int_name=mesa.name,
    int_type=mesa.int_type,
    aadt_major=aadt_major,
    aadt_minor=mesa.compute_minor_aadt(aadt_major, pct=mesa.minor_pct_default),
    scenario_name="Before - Low",
    aadt_max=aadt_limits,
    years=10
)
scenarios.append(before_low)
before_high = estimate_crashes(
    spfs=spfs,
    int_name=mesa.name,
    int_type=mesa.int_type,
    aadt_major=aadt_major,
    aadt_minor=mesa.compute_minor_aadt(aadt_major, pct=mesa.minor_pct_alt),
    scenario_name="Before - High",
    aadt_max=aadt_limits,
    years=10
)
scenarios.append(before_high)
after_low = estimate_crashes(
    spfs=spfs,
    int_name=mesa.name,
    int_type=mesa.int_type,
    aadt_major=aadt_major,
    aadt_minor=mesa.compute_minor_aadt(aadt_major, pct=mesa.minor_pct_default),
    scenario_name="After - Low",
    aadt_max=aadt_limits,
    years=10,
    bulbout_cmf=mesa.bulbout_default
)
scenarios.append(after_low)
after_high = estimate_crashes(
    spfs=spfs,
    int_name=mesa.name,
    int_type=mesa.int_type,
    aadt_major=aadt_major,
    aadt_minor=mesa.compute_minor_aadt(aadt_major, pct=mesa.minor_pct_alt),
    scenario_name="After - High",
    aadt_max=aadt_limits,
    years=10,
    bulbout_cmf=mesa.bulbout_default
)
scenarios.append(after_high)
logger.success("Mesa results completed")

logger.info("CREATING 4TH RESULTS")
before = estimate_crashes(
    spfs=spfs,
    int_name=fourth.name,
    int_type=fourth.int_type,
    aadt_major=aadt_major,
    aadt_minor=fourth.compute_minor_aadt(aadt_major, pct=fourth.minor_pct_default),
    scenario_name="Before - Indirect",
    aadt_max=aadt_limits,
    years=10
)
scenarios.append(before)
after_ind = estimate_crashes(
    spfs=spfs,
    int_name=fourth.name,
    int_type=fourth.int_type,
    aadt_major=aadt_major,
    aadt_minor=fourth.compute_minor_aadt(aadt_major, pct=fourth.minor_pct_alt),
    scenario_name="After - Indirect",
    aadt_max=aadt_limits,
    years=10,
    signal_cmf=fourth.signal_default
)
scenarios.append(after_ind)
after_dir = estimate_crashes(
    spfs=spfs,
    int_name=fourth.name,
    int_type=fourth.int_type_alt,
    aadt_major=aadt_major,
    aadt_minor=fourth.compute_minor_aadt(aadt_major, pct=fourth.minor_pct_alt),
    scenario_name="After - Direct",
    aadt_max=aadt_limits,
    pedvol=fourth.pedvol_default,
    nlanes=fourth.nlanes_default,
    years=10
)
scenarios.append(after_dir)
logger.success("4th results completed")

logger.info("Converting to Polars Dataframe")
df = pl.DataFrame(scenarios)
print(df)
logger.success("Dataframe created")
logger.info("Writing dataframe to csv")
name = datetime.today().strftime('%Y-%m-%d')
df.write_csv(f"data/results/results_{name}.csv")