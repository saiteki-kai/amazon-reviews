import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.category_barplot import category_barplot
from dashboard.components.category_sentiment_barplot import category_sentiment_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("categories-distribution", "figure"),
    Output("categories-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_brand_categories(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    order = dict(category=list(brand_df["category"].value_counts().index))
    return category_barplot(brand_df, order), category_sentiment_barplot(
        brand_df, order
    )


panel = html.Div(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id="categories-distribution"),
                className="h-100",
            ),
            dbc.Col(
                dcc.Graph(id="categories-distribution-perc"),
                className="h-100",
            ),
        ],
        className="h-100",
    ),
    className="panel",
)
