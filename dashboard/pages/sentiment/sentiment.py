import dash_bootstrap_components as dbc
from dash import html

from dashboard.pages.sentiment.panels import (
    category,
    sentiment,
    sentiment_over_time,
    topic,
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
                                    sentiment.panel,
                                    width=4,
                                    className="h-100",
                                ),
                                dbc.Col(
                                    category.panel,
                                    width=4,
                                    className="h-100",
                                ),
                                dbc.Col(
                                    topic.panel,
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
                                sentiment_over_time.panel,
                                width=8,
                                className="h-100",
                            ),
                            dbc.Col(
                                html.Div(className="panel"),
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
