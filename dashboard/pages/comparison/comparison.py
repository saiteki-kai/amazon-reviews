from collections import Counter

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

from dashboard.app import data_df, topic_set
from dashboard.utils import default_layout
from dashboard.pages.comparison.panels.topic_comparison import sentiment_aspect_df, topic_comparison



def global_sentiment_barplot(sentiment_df_perc, competitors, colors):
    # global sentiment
    fig2 = px.bar(
        sentiment_df_perc,
        y="brand",
        x="count",
        color="brand",
        barmode="relative",
        color_discrete_sequence=colors,
        category_orders=dict(brand=competitors),
        title="Sentiment By Brand",
    )
    fig2.update_layout(default_layout)
    fig2.update_layout(legend_orientation="v")
    fig2.update_xaxes(title_text="", ticksuffix="%")
    fig2.update_yaxes(title_text="")
    return fig2


def positive_sentiment_overtime_plot(brand, competitors, competitors_df, period, plotly_colors, sentiment_selected):
    # positive sentiment in time
    competitors_df["period"] = competitors_df["timestamp"].copy().dt.to_period(period)
    competitors_df["period"] = competitors_df["period"].dt.to_timestamp()

    sentiments_count = competitors_df.groupby(["period", "brand"])["sentiment"].value_counts()
    sentiments_df = pd.DataFrame(sentiments_count).rename(columns={"sentiment": "count"}).reset_index()
    total_reviews = sentiments_df.groupby(["period", "brand"])["count"].sum().reset_index()

    sentiments_df = pd.merge(sentiments_df, total_reviews, on=["period", "brand"])
    sentiments_df["percentage"] = sentiments_df["count_x"] / sentiments_df["count_y"] * 100

    fig3 = px.line(
        sentiments_df[sentiments_df['sentiment'] == sentiment_selected],
        x="period",
        y="percentage",
        color="brand",
        markers=True,
        category_orders=dict(brand=[brand, *competitors]),
        color_discrete_sequence=plotly_colors,
        title="Sentiment Over Time By Brand",
    )
    fig3.update_layout(default_layout)
    fig3.update_xaxes(showgrid=False, title_text="")
    fig3.update_yaxes(showgrid=False, title_text="% Reviews", ticksuffix="%")
    return fig3


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

            df_senti = st_counts.stack(level=0).reset_index().rename(columns={"level_1": "sentiment", 0: "count"})

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
    Output("brand_topics_1", "figure"),
    Output("brand_topics_2", "figure"),
    Output("brand_topics_3", "figure"),
    Output("brand_topics_4", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("sentiment-switch", "value"),
)
def update_plot(brand, category, sentiment):
    # costant parameters
    period = "Y"
    n_brand_to_keep = 4

    # update dataframe based on category
    category_df = data_df[data_df["category"] == category]

    # update dataframe based on brand
    category_df = category_df[category_df["brand"] != brand]

    # update sentiment selection
    sentiment_selected = 'positive' if sentiment else 'negative'

    # competitors selection by # of reviews
    competitors = list(category_df["brand"].value_counts().index)[:n_brand_to_keep]

    if brand not in competitors:
        competitors.pop()

    competitors = [brand] + competitors
    competitors_df = data_df[data_df["brand"].isin(competitors)]

    # sentiment perc
    sentiment_df = competitors_df.groupby("brand")["sentiment"].value_counts()
    sentiment_df_perc = sentiment_df / sentiment_df.groupby("brand").sum()
    sentiment_df_perc = pd.DataFrame(sentiment_df_perc * 100).rename(columns={"sentiment": "count"}).reset_index()
    sentiment_df_perc = sentiment_df_perc[sentiment_df_perc['sentiment'] == sentiment_selected]

    # sort competitors by positive sentiment perc
    competitors = list(sentiment_df_perc.sort_values(by='count', ascending=False)["brand"])

    # choose colors for competitors
    plotly_colors = ["#ECE81A", "#b5b4b1", "#8c8c8b", "#737372"]

    # comperison plots
    fig1 = global_sentiment_barplot(sentiment_df_perc, competitors, plotly_colors)
    fig2 = positive_sentiment_overtime_plot(brand, competitors, competitors_df, period, plotly_colors, sentiment_selected)

    topics = list(set(sentiment_aspect_df(competitors_df)["topic"].unique()))
    figures = []
    for i, competitor in enumerate(competitors):
        figures.append(topic_comparison(competitors_df, competitor, plotly_colors[i], topics, sentiment_selected))

    return fig1, fig2, *figures

@dash.callback(
    Output("sentiment-switch", "label"),
    [
        Input("sentiment-switch", "value"),
    ],
)
def on_sentiment_switch_change(sentiment_checked):
    if sentiment_checked:
        return 'Positive Sentiment'
    else:
        return 'Negative Sentiment'

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Switch(
                    id="sentiment-switch",
                    label="Positive Sentiment",
                    value=True,
                ),
                className="h-100",
            ),
            id="row-c1",
            className="g-0",
        ),
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
                        dcc.Graph(id="time_brand_pos_sentiment"),
                        className="panel",
                    ),
                    className="h-100",
                ),
            ],
            id="row-c2",
            className="g-0",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="brand_topics_1"),
                        className="panel",
                    ),
                    className="h-100",
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="brand_topics_2"),
                        className="panel",
                    ),
                    className="h-100",
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="brand_topics_3"),
                        className="panel",
                    ),
                    className="h-100",
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(id="brand_topics_4"),
                        className="panel",
                    ),
                    className="h-100",
                ),
            ],
            id="row-c3",
            className="g-0",
        ),
    ],
    className="page-container",
)
