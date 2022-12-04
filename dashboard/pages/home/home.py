import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

import dashboard.pages.home.brand_categories  # noqa:F401
import dashboard.pages.home.reviews_sentiment  # noqa:F401
import dashboard.pages.home.star_distribution  # noqa:F401
from dashboard.app import data_df
from dashboard.pages.home.sentiment_over_time import sentiment_over_time

# Brand Select
brand_select = dbc.Select(
    id="brand-select",
    options=[
        {"label": brand, "value": brand}
        for brand in list(data_df["brand"].value_counts().index)
    ],
    value="corsair",
)

# Brand Categories Select
category_select = dbc.Select(
    id="category-select",
    options=[],
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
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(brand_select, width=4),
                    dbc.Col(category_select, width=4),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(id="reviews-sentiment", width=4),
                    dbc.Col(id="star-distribution", width=4),
                ],
                justify="between",
            ),
            dbc.Row(dbc.Col(sentiment_over_time, width=6), justify="between"),
            html.Div(id="brand-categories"),
        ],
        fluid=True,
        className="py-3",
    ),
)
