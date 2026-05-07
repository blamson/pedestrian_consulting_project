import plotly.express as px

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

