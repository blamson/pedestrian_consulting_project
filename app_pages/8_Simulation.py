import streamlit as st
import polars as pl
from risk_estimation import crash_frequency_helpers as risk_mod, streamlit_helpers as helpers, plotting_helpers
from loguru import logger

title = "Simulating Long Term Risk"
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

# Reset simulation history if intersection changes
if "last_intersection_name" not in st.session_state:
    st.session_state.last_intersection_name = intersection.name

if st.session_state.last_intersection_name != intersection.name:
    del st.session_state["sim_history"]
    st.session_state.last_intersection_name = intersection.name
    all_sims = None
    button = None

# Debug info
if inputs.developer_view:
    helpers.show_debug(intersection, inputs)

# Results computation
results_df = (
    risk_mod.build_results_df(
        spf_table=spf_table,
        intersection=intersection,
        inputs=inputs,
        aadt_limit_table=aadt_limit_table
    )
)

st.header(f"Chance of an accident in a {inputs.years} year period.")
n_dashboard_cols = results_df.height
dashboard_cols = st.columns(n_dashboard_cols)
col_index = 0
for scenario in results_df.iter_rows(named=True):
    exp_acc = round(scenario["pred_ped"] * scenario["years"] * 100 ,2)
    scenario_name = scenario["scenario"]
    dashboard_cols[col_index].metric(
        f"{scenario_name}",
        value=f"{exp_acc}%",
        border=True
    )
    col_index += 1


if "sim_history" not in st.session_state:
    st.session_state.sim_history = []

button = st.button("Run a single simulation", type="primary")
col1, col2 = st.columns(2)
if button:
    logger.info("Running simulation")
    simulated_df = risk_mod.simulate_accidents_over_time(results_df)
    st.session_state.sim_history.append(simulated_df)
    n_dashboard_cols = results_df.height
    for scenario in simulated_df.iter_rows(named=True):
        scenario_name = scenario["scenario"]
        col1.metric(
            f"{scenario_name}",
            value=scenario["simulated_total_crashes"],
            border=True
        )
    logger.success(f"Simulation complete - Total simulations: {len(st.session_state.sim_history)}")


if len(st.session_state.sim_history) > 0:
    logger.info("Collecting all simulation results")
    all_sims = pl.concat(st.session_state.sim_history, how="vertical_relaxed")
    col1.metric(
        "Number of simulations ran",
        value=int(all_sims.height / results_df.height),
        border=True
    )

    agg_df = (
        all_sims
        .group_by("scenario")
        .agg(
            pl.col("simulated_total_crashes").sum().alias("total_crashes")
        )
    )
    logger.success("Simulation results collected as polars dataframe")
else:
    agg_df = None

if agg_df is not None:
    logger.info("Creating simulation barplot")
    scenario_order = results_df["scenario"].to_list()
    fig, key = plotting_helpers.make_accident_bar(
        agg_df, 
        title="Number of crashes - Running Total",
        y_col="total_crashes",
        y_label="Number of crashes",
        key="single_simulation_plot",
        scenario_order=scenario_order
    )
    fig.update_yaxes(rangemode="tozero")
    fig.update_layout(
        xaxis=dict(
            categoryorder="array",
            categoryarray=scenario_order
        )
    )
    col2.plotly_chart(fig)
    logger.success("Simulation barplot created")

text = helpers.load_text("app_pages/text_files/dashboard/simulations.md")
if st.toggle("Show explanation?"):
    st.markdown(text)