import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def generate_boxplot(df, x, y, points, color, color_discrete_map):
    fig = px.box(
        df,
        x=x,
        y=y,
        points=points,
        color=color,
        color_discrete_map=color_discrete_map,
    )
    return fig


def generate_overlaid_histogram(traces, names, colors):
    fig = go.Figure()
    for trace, name, color in zip(traces, names, colors):
        fig.add_trace(
            go.Histogram(x=trace, name=name, marker_color=color, xbins={"size": 5})
        )
    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.75)
    return fig


def generate_ranking_plot(df, input_col, options, scoring):
    input_col_score = pd.Series(index=options)
    for i in range(1, 7):
        input_col_counts = df[f"{input_col}[{i}]"].value_counts()
        scores = input_col_counts.multiply(scoring[i])
        input_col_score = input_col_score.add(scores, fill_value=0)
        input_col_score = input_col_score.sort_values(ascending=False)
        if i == 1:
            ranked_first = df[f"{input_col}[1]"].value_counts()
            ranked_first_clean = pd.DataFrame(
                {"institution": ranked_first.index, "ranked_first": ranked_first.values}
            )
    input_col_df = pd.DataFrame(
        {
            "institution": input_col_score.index,
            "score": input_col_score.values,
        }
    )
    input_col_df = input_col_df.merge(
        ranked_first_clean, on="institution", how="left"
    ).fillna(0)
    input_col_df = input_col_df.sort_values(["score", "ranked_first"])
    fig = px.bar(
        input_col_df.sort_values(by="score"),
        y="institution",
        x="score",
        color="ranked_first",
        color_continuous_scale="viridis",
        orientation="h",
    )
    return fig
