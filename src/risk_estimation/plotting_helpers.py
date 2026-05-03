import plotly.express as px

def make_accident_bar(df, y_col, title, y_label, color_map, key):

    # if not show_y_axis_label:

    fig = px.bar(
        df,
        x="scenario",
        y=y_col,
        text=y_col,
        title=title,
        labels={
            "scenario": "Scenario",
            y_col: y_label,
        },
        hover_data={y_col: ':.3f'}
    )

    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:.3f}",
        # marker=dict(color=[color_map[s] for s in df["scenario"]])
        marker=dict(color=px.colors.qualitative.Vivid)
    )

    return fig, key