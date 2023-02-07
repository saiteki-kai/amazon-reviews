import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from plotly import express as px

from dashboard.app import data_df
from dashboard.utils import default_layout, secondary_color, update_brand


@dash.callback(
    Output("reviews-over-time", "figure"),
    Input("home-period", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def plot_reviews_over_time(period, brand, category, from_year, to_year):
    # update graph brand
    brand_df = update_brand(data_df, brand, category, from_year, to_year)

    brand_df[period] = brand_df["timestamp"].dt.to_period(period)
    brand_df[period] = brand_df[period].dt.to_timestamp()

    x = pd.DataFrame(brand_df[period].value_counts().reset_index().rename(columns={"index": "period", period: "count"}))
    x.sort_values(by="period", inplace=True)

    fig = px.area(
        x,
        x="period",
        y="count",
        markers=True,
        color_discrete_sequence=[secondary_color],
        title="Reviews Over Time",
    )

    fig.update_layout(default_layout)
    fig.update_layout(legend_orientation="v", margin=dict(t=40))
    # fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_yaxes(title_text="# Reviews")

    return fig


panel = html.Div(
    [
        dcc.Graph(id="reviews-over-time", config={"displayModeBar": False}),
        dbc.Select(
            id="home-period",
            className="floating-select",
            options=[
                {"label": "Day", "value": "D"},
                {"label": "Week", "value": "W"},
                {"label": "Month", "value": "M"},
                {"label": "Year", "value": "Y"},
            ],
            value="M",
            size="sm",
        ),
    ],
    className="panel",
    style={"position": "relative"},
)
