import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.pages.home.panels import (
    brand_categories,
    measures,
    sentiment_over_time,
    star_distribution,
    topics_sentiment,
    word_cloud,
)


@dash.callback(
    Output("category-select", "options"),
    Output("category-select", "value"),
    Input("brand-select", "value"),
)
def update_categories(brand):
    df = data_df[data_df["brand"] == brand]

    categories = list(df["category"].value_counts().index)
    options = [{"label": c, "value": c} for c in categories]

    options = [{"label": "All", "value": "All"}] + options

    return options, "All"


layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                measures.panel,
                                className="h-100",
                            ),
                            dbc.Col(
                                star_distribution.panel,
                                className="h-100",
                            ),
                        ],
                        id="row1",
                        className="g-0",
                    ),
                    dbc.Row(
                        dbc.Col(sentiment_over_time.panel, className="h-100"),
                        id="row2",
                        className="g-0",
                    ),
                ],
                width=6,
                className="h-100",
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            brand_categories.panel,
                            className="h-100",
                        ),
                        id="row3",
                        className="g-0",
                    ),
                    dbc.Row(
                        dbc.Col(
                            topics_sentiment.panel,
                            className="h-100",
                        ),
                        id="row4",
                        className="g-0",
                    ),
                    dbc.Row(
                        dbc.Col(
                            word_cloud.panel,
                            className="h-100",
                        ),
                        id="row5",
                        className="g-0",
                    ),
                ],
                width=6,
                className="h-100",
            ),
        ],
        className="h-100 g-0",
    ),
    className="page-container",
)
