import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.utils import update_brand


def star_row(df, n):
    n_reviews = len(df)
    overall_perc = len(df[df["overall"] == n]) / n_reviews * 100
    stars_icon = [html.I(className="fa-solid fa-star mx-1") for _ in range(n)]

    return html.Div(
        [
            dbc.Row([dbc.Col(html.H3(f"{overall_perc:.1f}%"))]),
            dbc.Row(
                [
                    dbc.Col([f"{len(df[df['overall'] == n])} Reviews"]),
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
                        color="gray",
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
    return html.Div([star_row(brand_df, i) for i in range(5, 0, -1)])
