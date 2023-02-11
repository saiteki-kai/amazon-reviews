import dash
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.category_sentiment_barplot import category_sentiment_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("categories-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def update_brand_categories(brand, category, from_year, to_year):
    # update graph brand
    brand_df = update_brand(data_df, brand, category, from_year, to_year)

    return category_sentiment_barplot(brand_df)


panel = html.Div(
    dcc.Graph(id="categories-distribution-perc", config={"displayModeBar": False}),
    className="panel",
)
