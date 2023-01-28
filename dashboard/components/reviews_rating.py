import dash_bootstrap_components as dbc
import humanize
import numpy as np
from dash import html


def last_year_sentiment(polarity="positive", perc=0):
    icon = "fa-arrow-down" if perc < 0 else "fa-arrow-up"
    color = "green" if polarity == "positive" else "red"

    return html.Span(
        [
            html.I(className=f"fa-solid {icon} mx-1"),
            f"{abs(perc):.0f}%",
            html.Span(
                " (from last year)",
                style={"color": "var(--bs-body-color)"},
            ),
        ],
        style={"color": color},
    )


def total_sentiment(polarity="positive", count=0, last_year_perc=0):
    return [
        html.H3(polarity.capitalize()),
        html.Span(
            [
                html.Span(
                    f"{humanize.intcomma(count)}",
                    style={"fontSize": "1.5em"},
                ),
                last_year_sentiment(polarity, perc=last_year_perc),
            ],
        ),
    ]


def reviews_rating(brand_df):
    n_reviews = len(brand_df)
    n_positive = len(brand_df[brand_df["sentiment"] == "positive"])
    n_negative = n_reviews - n_positive

    last_days = brand_df["timestamp"].max() - np.timedelta64(1, "Y")

    old_year_df = brand_df[brand_df["timestamp"] < last_days]
    old_n_negative = len(old_year_df[old_year_df["sentiment"] == "negative"])
    old_n_positive = len(old_year_df[old_year_df["sentiment"] == "positive"])

    pos_perc = np.round(n_positive / n_reviews * 100)

    last_year_pos_perc = int((n_positive - old_n_positive) / n_positive * 100)
    last_year_neg_perc = int((n_negative - old_n_negative) / n_negative * 100)

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H1("Reviews")),
                    dbc.Col(
                        html.H1(
                            humanize.intcomma(n_reviews),
                            style={"textAlign": "right"},
                        ),
                    ),
                ],
                justify="between",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        total_sentiment(
                            "positive",
                            n_positive,
                            last_year_pos_perc,
                        ),
                    ),
                    dbc.Col(
                        total_sentiment(
                            "negative",
                            n_negative,
                            last_year_neg_perc,
                        ),
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
        ],
    )
