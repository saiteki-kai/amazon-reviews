import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from plotly import express as px

from dashboard.app import data_df
from dashboard.utils import update_brand


@dash.callback(
    Output("sentiment-over-time", "figure"),
    Input("period", "value"),
    Input("years-slider", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def plot_sentiment_over_time(period, years, brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    brand_df[period] = brand_df["timestamp"].dt.to_period(period)
    brand_df[period] = brand_df[period].dt.to_timestamp()

    sentiments_count = brand_df.groupby(period)["sentiment"].value_counts()
    sentiments_df = (
        pd.DataFrame(sentiments_count)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig = px.line(
        sentiments_df,
        x=period,
        y="count",
        color="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        title="Sentiment Over Time",
    )
    fig.update_xaxes(
        showgrid=False,
        title_text="",
        range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig.update_yaxes(showgrid=False, title_text="# Reviews")
    fig.update_layout(margin=dict(l=0, r=0, b=0))

    return fig


@dash.callback(
    Output("years-slider", "min"),
    Output("years-slider", "max"),
    Output("years-slider", "step"),
    Output("years-slider", "marks"),
    Output("years-slider", "value"),
    Input("period", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_ranges(period, brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    dates = brand_df["timestamp"].dt.to_period(period).dt.to_timestamp()
    min_year = dates.min().year
    max_year = dates.max().year

    marks = {i: str(i) for i in range(min_year, max_year + 1, 1)}

    return (
        min_year,
        max_year,
        1,
        marks,
        [min_year, max_year],
    )


panel = html.Div(
    [
        dcc.Graph(id="sentiment-over-time"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.RangeSlider(
                        1999, 2018, 1, value=[1999, 2018], id="years-slider"
                    )
                ),
                dbc.Col(
                    [
                        dbc.Select(
                            id="period",
                            options=[
                                {"label": "Day", "value": "D"},
                                {"label": "Week", "value": "W"},
                                {"label": "Month", "value": "M"},
                                {"label": "Year", "value": "Y"},
                            ],
                            value="Y",
                        ),
                    ],
                    width=2,
                ),
            ]
        ),
    ],
    className="panel",
)
