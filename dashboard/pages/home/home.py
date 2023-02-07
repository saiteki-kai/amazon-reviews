import dash_bootstrap_components as dbc
from dash import html

from dashboard.pages.home.panels import (
    categories,
    reviews_over_time,
    star_distribution,
    topics,
    word_cloud,
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    star_distribution.panel,
                                    width=4,
                                    className="h-100",
                                ),
                                dbc.Col(
                                    categories.panel,
                                    width=4,
                                    className="h-100",
                                ),
                                dbc.Col(
                                    topics.panel,
                                    width=4,
                                    className="h-100",
                                ),
                            ],
                            id="row1",
                            className="h-100 g-0",
                        ),
                    ],
                    className="h-100",
                ),
            ],
            id="row1",
            className="g-0",
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                reviews_over_time.panel,
                                width=8,
                                className="h-100",
                            ),
                            dbc.Col(
                                word_cloud.panel,
                                width=4,
                                className="h-100",
                            ),
                        ],
                        id="row1",
                        className="h-100 g-0",
                    ),
                ],
                className="h-100",
            ),
            id="row2",
            className="g-0",
        ),
    ],
    className="page-container",
)
