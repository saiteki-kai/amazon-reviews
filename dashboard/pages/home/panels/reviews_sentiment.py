import dash
from dash import Input, Output

from dashboard.app import data_df
from dashboard.components.reviews_rating import reviews_rating
from dashboard.utils import update_brand


@dash.callback(
    Output("reviews-sentiment", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def update_reviews_sentiment(brand, category, from_year, to_year):
    # update graph brand
    brand_df = update_brand(data_df, brand, category, from_year, to_year)

    return reviews_rating(brand_df)
