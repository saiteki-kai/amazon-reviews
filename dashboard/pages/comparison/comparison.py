from collections import Counter

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

from dashboard.app import data_df, topic_set


@dash.callback(
    Output("topic_dropdown", "options"),
    Output("topic_dropdown", "value"),
    Input("category-select", "value"),
)
def update_category(category):
    opt = [{"label": f"{i}", "value": f"{i}"} for i in topic_set]
    return opt, opt[0]["value"]


def global_sentiment_barplot(brand, competitors, competitors_df):
    # global sentiment
    sentiment_df = competitors_df.groupby("brand")["sentiment"].value_counts()
    sentiment_df_perc = sentiment_df / sentiment_df.groupby("brand").sum()
    sentiment_df_perc = (
        pd.DataFrame(sentiment_df_perc * 100)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig2 = px.bar(
        sentiment_df_perc,
        x="brand",
        y="count",
        color="sentiment",
        barmode="relative",
        category_orders=dict(brand=[brand, *competitors]),
    )
    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig2.update_layout(margin=dict(l=0, t=0, r=0, b=0))
    return fig2


def positive_sentiment_overtime_plot(period, competitors_df):
    # positive sentiment in time
    competitors_df[period] = competitors_df["timestamp"].dt.to_period(period)
    competitors_df[period] = competitors_df[period].dt.to_timestamp()

    sentiments_count = (
        competitors_df[competitors_df["sentiment"] == "positive"]
        .groupby([period, "brand"])["sentiment"]
        .value_counts()
    )
    sentiments_df = (
        pd.DataFrame(sentiments_count)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig3 = px.line(
        sentiments_df,
        x=period,
        y="count",
        color="brand",
        # title="Sentiment Over Time",
    )
    fig3.update_xaxes(
        showgrid=False,
        title_text="",
        # range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig3.update_yaxes(showgrid=False, title_text="# Reviews")
    fig3.update_layout({"margin": dict(l=0, r=0, b=0)})
    return fig3


def negative_sentiment_overtime_plot(period, competitors_df):
    # negative sentiment in time
    sentiments_count = (
        competitors_df[competitors_df["sentiment"] == "negative"]
        .groupby([period, "brand"])["sentiment"]
        .value_counts()
    )
    sentiments_df = (
        pd.DataFrame(sentiments_count)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig4 = px.line(
        sentiments_df,
        x=period,
        y="count",
        color="brand",
        # title="Sentiment Over Time",
    )
    fig4.update_xaxes(
        showgrid=False,
        title_text="",
        # range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig4.update_yaxes(showgrid=False, title_text="# Reviews")
    fig4.update_layout({"margin": dict(l=0, r=0, b=0)})
    return fig4


def sentiment_topic_plot(brand, competitors, competitors_df):
    # sentimenti for topic
    total_df = pd.DataFrame()

    for brand in competitors:
        pos_count = Counter()
        neg_count = Counter()

        brand_df = competitors_df[competitors_df["brand"] == brand]
        for t in brand_df["topics"].values:
            pos_topics = set([s["name"] for s in t if s["sentiment"] == 0])
            neg_topics = set([s["name"] for s in t if s["sentiment"] == 1])

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

            df_senti = (
                st_counts.stack(level=0)
                .reset_index()
                .rename(columns={"level_1": "sentiment", 0: "count"})
            )

            df_senti["brand"] = brand

            total_df = pd.concat((df_senti, total_df))
            total_df = total_df[total_df["topic"] == t]

    fig5 = px.bar(
        total_df,
        x="brand",
        y="count",
        color="sentiment",
        barmode="relative",
        category_orders=dict(brand=[brand, *competitors]),
    )
    fig5.update_xaxes(showgrid=False, title_text="")
    fig5.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig5.update_layout(margin=dict(l=0, t=0, r=0, b=0))
    return fig5


@dash.callback(
    Output("global_sentiment", "figure"),
    Output("time_brand_pos_sentiment", "figure"),
    Output("time_brand_neg_sentiment", "figure"),
    Output("topic_sentiment", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("topic_dropdown", "value"),
)
def update_plot(brand, category, topic):
    category_df = data_df[data_df["category"] == category]
    category_df = category_df[category_df["brand"] != brand]

    period = "Y"

    # competitors
    competitors = list(category_df["brand"].value_counts().index)[:5] + [brand]
    competitors_df = data_df[data_df["brand"].isin(competitors)]

    fig2 = global_sentiment_barplot(brand, competitors, competitors_df)
    fig3 = positive_sentiment_overtime_plot(period, competitors_df)
    fig4 = negative_sentiment_overtime_plot(period, competitors_df)
    fig5 = sentiment_topic_plot(brand, competitors, competitors_df)
    return fig2, fig3, fig4, fig5


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="global_sentiment"),
                        className="panel",
                    ),
                    className="h-100",
                ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="topic_dropdown",
                                options=[""],
                                placeholder="select topic",
                                value="Gold",
                                clearable=False,
                            ),
                            dcc.Graph(id="topic_sentiment"),
                        ],
                        className="panel",
                    ),
                    className="h-100",
                ),
            ],
            id="row1",
            className="g-0",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="time_brand_pos_sentiment"),
                        className="panel",
                    ),
                    className="h-100",
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="time_brand_neg_sentiment"),
                        className="panel",
                    ),
                    className="h-100",
                ),
            ],
            id="row2",
            className="g-0",
        ),
    ],
    className="page-container",
)
