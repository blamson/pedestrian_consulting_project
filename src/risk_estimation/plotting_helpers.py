import plotly.express as px
import streamlit as st

def make_accident_bar(df, y_col, title, y_label, key, scenario_order):

    fig = px.bar(
        df,
        x="scenario",
        y=y_col,
        # barmode="group",
        text=y_col,
        title=title,
        labels={
            "scenario": "Scenario",
            y_col: y_label,
        },
        hover_data={y_col: ':.3f'},
        color="scenario",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        category_orders={"scenario": scenario_order}
    )

    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:.3f}"
    )

    fig.update_layout(showlegend=False)

    return fig, key


# For sure w/ the accident rate tab. may make more modular?
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