import dash
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.category_sentiment_barplot import category_sentiment_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("categories-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_brand_categories(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    order = dict(category=list(brand_df["category"].value_counts().index))

    return category_sentiment_barplot(brand_df, order)


panel = html.Div(
    dcc.Graph(id="categories-distribution-perc", config={"displayModeBar": False}),
    className="panel",
)
