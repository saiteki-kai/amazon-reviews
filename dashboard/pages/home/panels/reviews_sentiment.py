import dash
from dash import Input, Output

from dashboard.app import data_df
from dashboard.components.reviews_rating import reviews_rating
from dashboard.utils import update_brand


@dash.callback(
    Output("reviews-sentiment", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_reviews_sentiment(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    return reviews_rating(brand_df)
