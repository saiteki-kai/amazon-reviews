import dash
import dash_bootstrap_components as dbc
import humanize
import numpy as np
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.utils import update_brand


def star_row(df, n):
    n_reviews = len(df[df["overall"] == n])

    overall_perc = n_reviews / len(df) * 100
    stars_icon = [html.I(className="fa-solid fa-star") for _ in range(n)]

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H6(f"{overall_perc:.1f}%", className="m-0")),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.P(
                            f"{humanize.intcomma(n_reviews)} Reviews",
                            className="m-0",
                        )
                    ),
                    dbc.Col(
                        stars_icon,
                        style={"textAlign": "right"},
                    ),
                ]
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Progress(
                        value=np.round(overall_perc),
                        color="#108de4",
                        style={"height": "8px"},
                    ),
                ),
            ),
        ],
    )


@dash.callback(
    Output("star-distribution", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def star_distribution(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    return [star_row(brand_df, i) for i in range(5, 0, -1)]


panel = html.Div(
    [
        html.H4("Star Distribution"),
        html.Div(id="star-distribution"),
    ],
    className="panel",
)
