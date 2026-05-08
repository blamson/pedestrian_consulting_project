import plotly.express as px
import polars as pl
import streamlit as st

def make_accident_bar(df, y_col, title, y_label, key, scenario_order, x_col="scenario", barmode=None, legend=False, x_label="Scenario", rounding_format=".3f"):

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        text=y_col,
        title=title,
        labels={
            x_col: x_label,
            y_col: y_label,
        },
        hover_data={y_col: rounding_format},
        color="scenario",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        category_orders={"scenario": scenario_order}
    )

    fig.update_traces(
        textposition="outside",
        texttemplate=f"%{{y:{rounding_format}}}"
    )

    if not legend:
        fig.update_layout(showlegend=False)
    if barmode is not None:
        fig.update_layout(barmode=barmode)

    return fig, key


# For use w/ the accident rate tab. may make more modular?
def render_charts(df, key_prefix):
    scenario_order = df["scenario"].to_list()

    col1, col2 = st.columns(2)

    fig1, key1 = make_accident_bar(
        df,
        y_col="pred_ped",
        title="Pedestrian Accident Rate",
        y_label="Accidents per Year",
        key=f"{key_prefix}_ped",
        scenario_order=scenario_order
    )

    fig2, key2 = make_accident_bar(
        df,
        y_col="pred_veh",
        title="Vehicle Accident Rate",
        y_label="Accidents per Year",
        key=f"{key_prefix}_veh",
        scenario_order=scenario_order
    )

    col1.plotly_chart(fig1, key=key1)
    col2.plotly_chart(fig2, key=key2)


def render_long_term_risk(df, prefix, years=10):
    col1, col2 = st.columns(2)

    # --- bar chart (single-year snapshot)
    fig_bar = px.bar(
        df.filter(pl.col("years") == years),
        x="scenario",
        y="long_run_ped_percent",
        text="long_run_ped_percent",
        title=f"Chance of at least one accident in {years} years",
        labels={
            "scenario": "Scenario",
            "long_run_ped_percent": "Chance of an accident (%)"
        }
    )

    fig_bar.update_traces(
        textposition="outside",
        texttemplate="%{text:.0f}%",
        marker=dict(color=px.colors.qualitative.Vivid)
    )
    fig_bar.update_layout(yaxis_range=[0, 100])

    col1.plotly_chart(fig_bar, key=f"{prefix}_bar")

    # --- line chart (trajectory)
    fig_line = px.line(
        df,
        x="years",
        y="long_run_ped_percent",
        color="scenario",
        title="Chance of at least one accident over time",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={
            "years": "Years",
            "scenario": "Scenario",
            "long_run_ped_percent": "Chance of an accident (%)"
        }
    )

    fig_line.add_vline(
        x=years,
        line_width=1,
        line_dash="dash",
        line_color="red",
        opacity=0.7,
        annotation_text=f"Year Selected: {years}"
    )

    fig_line.update_traces(mode="markers+lines", hovertemplate=None)
    fig_line.update_layout(
        yaxis_range=[0, 100],
        legend=dict(
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.99
        ),
        hovermode="x"
    )

    fig_line.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikethickness=1,
        spikecolor="grey"
    )

    col2.plotly_chart(fig_line, key=f"{prefix}_line")