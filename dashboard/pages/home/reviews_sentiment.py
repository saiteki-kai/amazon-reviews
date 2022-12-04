import dash
import dash_bootstrap_components as dbc
import humanize
import numpy as np
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.utils import update_brand


@dash.callback(
    Output("reviews-sentiment", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_reviews_sentiment(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    n_reviews = len(brand_df)
    n_positive = len(brand_df[brand_df["sentiment"] == "positive"])
    last_days = brand_df["timestamp"].max() - np.timedelta64(1, "Y")

    old_year_df = brand_df[brand_df["timestamp"] < last_days]
    old_n_negative = len(old_year_df[old_year_df["sentiment"] == "negative"])
    old_n_positive = len(old_year_df[old_year_df["sentiment"] == "positive"])

    pos_perc = np.round(n_positive / n_reviews * 100)

    positive_perc = html.Span(
        [
            html.I(className="fa-solid fa-arrow-up mx-1"),
            f"{((n_positive - old_n_positive) / n_positive * 100):.0f}%",
            html.Span(
                " (from last year)",
                style={"color": "var(--bs-body-color)"},
            ),
        ],
        style={"color": "green"},
    )

    n_negative = n_reviews - n_positive
    negative_perc = html.Span(
        [
            html.I(className="fa-solid fa-arrow-down mx-1"),
            f"{(n_negative - old_n_negative) / n_negative * 100:.0f}%",
            html.Span(
                " (from last year)",
                style={"color": "var(--bs-body-color)"},
            ),
        ],
        style={"color": "red"},
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H1("Reviews")),
                    dbc.Col(
                        html.H1(
                            humanize.intcomma(
                                n_reviews
                            ),  # humanize.intword(n_reviews, format="%.0f")
                            style={"textAlign": "right"},
                        ),
                    ),
                ],
                justify="between",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Positive"),
                            html.Span(
                                [
                                    html.Span(
                                        f"{humanize.intcomma(n_positive)}",
                                        style={"fontSize": "1.5em"},
                                    ),
                                    positive_perc,
                                ],
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.H3("Negative"),
                            html.Span(
                                [
                                    html.Span(
                                        f"{humanize.intcomma(n_negative)}",
                                        style={"fontSize": "1.5em"},
                                    ),
                                    negative_perc,
                                ]
                            ),
                        ],
                        style={"textAlign": "right"},
                    ),
                ],
                justify="between",
                class_name="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Progress(
                            [
                                dbc.Progress(
                                    value=pos_perc,
                                    color="success",
                                    bar=True,
                                ),  # , label=f"\t{pos_perc:.1f}%"),
                                dbc.Progress(
                                    value=100 - pos_perc,
                                    color="danger",
                                    bar=True,
                                ),  # , label=f"\t{100 - pos_perc:.1f}%"),
                            ],
                        ),
                    ),
                ]
            ),
        ]
    )
