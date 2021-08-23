import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def generate_pie_chart(
    df,
    values,
    names,
    hover_name,
    color,
    color_discrete_sequence,
    color_discrete_map,
):
    fig = px.pie(
        df,
        values=values,
        names=names,
        hover_name=hover_name,
        color=color,
        color_discrete_sequence=color_discrete_sequence,
        color_discrete_map=color_discrete_map,
        width=800,
    )
    fig.update_traces(textinfo="percent+value")
    return fig


def generate_histogram(df, x, y, nbins, color, color_discrete_map, labels):
    fig = px.histogram(
        df,
        x=x,
        y=y,
        nbins=nbins,
        color=color,
        color_discrete_map=color_discrete_map,
        labels=labels,
    )
    return fig


def generate_overlaid_histogram(traces, names, colors):
    fig = go.Figure()
    for trace, name, color in zip(traces, names, colors):
        fig.add_trace(go.Histogram(x=trace, name=name, marker_color=color))
    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.75)
    return fig


def generate_stacked_bar_chart(data):
    fig = go.Figure(data=data)
    fig.update_layout(width=800, height=800, barmode="stack")
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
