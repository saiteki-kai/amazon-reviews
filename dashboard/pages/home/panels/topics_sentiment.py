from collections import Counter

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.utils import update_brand


@dash.callback(
    Output("topics-distribution", "figure"),
    Output("topics-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_topics_sentiment(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    count = Counter()
    for x in brand_df["topics"].values:
        topics = set(["T" + str(y["topic"]) for y in x])
        count.update(topics)

    topics_count = pd.DataFrame(count.items(), columns=["topic", "count"])
    topics_count["topic"] = topics_count["topic"].astype("category")

    order = topics_count.sort_values(by="count", ascending=False)
    order = order.reset_index()["topic"]

    fig1 = px.bar(
        topics_count,
        y="topic",
        x="count",
        color_discrete_sequence=["#108de4"],
        category_orders=dict(topic=order),
    )
    fig1.update_xaxes(showgrid=False, title_text="")
    fig1.update_yaxes(showgrid=False, title_text="")
    fig1.update_layout({"margin": dict(l=0, t=0, r=0, b=0)})

    pos_count = Counter()
    neg_count = Counter()

    for t in brand_df["topics"].values:
        pos_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 0])
        neg_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 1])

        pos_count.update(pos_topics)
        neg_count.update(neg_topics)

    pos_df = pd.DataFrame(pos_count.items(), columns=["topic", "pos"])
    neg_df = pd.DataFrame(neg_count.items(), columns=["topic", "neg"])

    st_counts = pd.merge(pos_df, neg_df, on="topic")
    st_counts["topic"] = st_counts["topic"].astype("category")

    total = st_counts["pos"] + st_counts["neg"]
    st_counts["pos"] = st_counts["pos"] / total * 100
    st_counts["neg"] = st_counts["neg"] / total * 100

    st_counts.set_index("topic", inplace=True)
    st_counts.sort_index(inplace=True)
    st_counts = st_counts.iloc[[int(o[1:]) for o in order][::-1]]

    df_senti = (
        st_counts.stack(level=0)
        .reset_index()
        .rename(columns={"level_1": "sentiment", 0: "count"})
    )

    fig2 = px.bar(
        df_senti,
        y="topic",
        x="count",
        color="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        barmode="relative",
        category_orders=dict(topic=order),
    )

    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="")
    fig2.update_layout({"margin": dict(l=0, t=0, r=0, b=0)})

    return fig1, fig2


panel = html.Div(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id="topics-distribution"),
                className="h-100",
            ),
            dbc.Col(
                dcc.Graph(id="topics-distribution-perc"),
                className="h-100",
            ),
        ],
        className="h-100",
    ),
    className="panel",
)
