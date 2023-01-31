import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from plotly import express as px

from dashboard.app import data_df
from dashboard.utils import secondary_color, update_brand


@dash.callback(
    Output("reviews-over-time", "figure"),
    Input("home-period", "value"),
    Input("home-years-slider", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def plot_reviews_over_time(period, years, brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    brand_df[period] = brand_df["timestamp"].dt.to_period(period)
    brand_df[period] = brand_df[period].dt.to_timestamp()

    x = pd.DataFrame(
        brand_df[period]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "period", period: "count"})
    )
    x.sort_values(by="period", inplace=True)

    fig = px.line(
        x,
        x="period",
        y="count",
        color_discrete_sequence=[secondary_color],
        title="Reviews Over Time",
    )
    fig.update_xaxes(
        showgrid=False,
        title_text="",
        range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig.update_yaxes(showgrid=False, title_text="# Reviews")
    fig.update_layout(margin=dict(l=0, t=30, r=0, b=0), title_pad=dict(t=0, b=0))

    return fig


@dash.callback(
    Output("home-years-slider", "min"),
    Output("home-years-slider", "max"),
    Output("home-years-slider", "step"),
    Output("home-years-slider", "marks"),
    Output("home-years-slider", "value"),
    Input("home-period", "value"),
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
        dcc.Graph(id="reviews-over-time"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.RangeSlider(
                        1999,
                        2018,
                        1,
                        value=[1999, 2018],
                        id="home-years-slider",
                    )
                ),
                dbc.Col(
                    [
                        dbc.Select(
                            id="home-period",
                            options=[
                                {"label": "Day", "value": "D"},
                                {"label": "Week", "value": "W"},
                                {"label": "Month", "value": "M"},
                                {"label": "Year", "value": "Y"},
                            ],
                            className="pe-0",
                            value="Y",
                            size="sm",
                        ),
                    ],
                    width=2,
                ),
            ],
            className="pt-1",
        ),
    ],
    className="panel",
)
