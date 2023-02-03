import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from plotly import express as px

from dashboard.app import data_df
from dashboard.utils import default_layout, update_brand


@dash.callback(
    Output("sentiment-over-time", "figure"),
    Input("period", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("year-select", "value"),
)
def plot_sentiment_over_time(period, brand, category, year):
    # update graph brand
    brand_df = update_brand(data_df, brand, category, year)

    brand_df["period"] = brand_df["timestamp"].dt.to_period(period)
    brand_df["period"] = brand_df["period"].dt.to_timestamp()

    sentiments_count = brand_df.groupby("period")["sentiment"].value_counts()
    sentiments_df = pd.DataFrame(sentiments_count).rename(columns={"sentiment": "count"}).reset_index()
    total_reviews = sentiments_df.groupby("period")["count"].sum().reset_index()

    sentiments_df = pd.merge(sentiments_df, total_reviews, on="period")
    sentiments_df["percentage"] = sentiments_df["count_x"] / sentiments_df["count_y"] * 100

    fig = px.area(
        sentiments_df,
        x="period",
        y="percentage",
        color="sentiment",
        markers=True,
        category_orders={"sentiment": ["positive", "negative"]},
        color_discrete_sequence=["#27d957", "#f54242"],
        title="Sentiment Over Time",
    )

    fig.update_layout(default_layout)
    fig.update_layout(legend_orientation="v", margin=dict(t=40))
    fig.update_xaxes(dtick="M1", tickformat="%b")
    fig.update_yaxes(title_text="% Reviews", ticksuffix="%")

    return fig


panel = html.Div(
    [
        dcc.Graph(id="sentiment-over-time", config={"displayModeBar": False}),
        dbc.Select(
            id="period",
            className="floating-select pe-0",
            options=[
                {"label": "Day", "value": "D"},
                {"label": "Week", "value": "W"},
                {"label": "Month", "value": "M"},
            ],
            value="M",
            size="sm",
        ),
    ],
    className="panel",
    style={"position": "relative"},
)