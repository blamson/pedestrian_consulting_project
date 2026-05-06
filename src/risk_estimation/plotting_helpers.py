import plotly.express as px
import polars as pl

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


def make_accident_bar_new(df, y_col, title, y_label, key):

    # if not show_y_axis_label:

    fig = px.bar(
        df,
        x="scenario",
        y=y_col,
        # color="ped_estimation_type",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        text=y_col,
        title=title,
        labels={
            "scenario": "Scenario",
            y_col: y_label
            # "ped_estimation_type": "Pedestrian Estimation Type"
        },
        hover_data={y_col: ':.3f'}
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:.3f}"
    )

    # n_estimation_types = df.select(pl.col("ped_estimation_type").n_unique()).item()
    # if n_estimation_types == 1:
    #     fig.update_layout(showlegend=False)
    # else:
    #     fig.update_layout(legend=dict(
    #         orientation="h",
    #         entrywidth=70,
    #         yanchor="bottom",
    #         y=1.02,
    #         xanchor="right",
    #         x=1
    #     ))

    return fig, key