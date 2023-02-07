import dash
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.components.worcloud import wordcloud
from dashboard.utils import update_brand


@dash.callback(
    Output("wordcloud-img", "src"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def update_word_cloud(brand, category, from_year, to_year):
    # update graph brand
    brand_df = update_brand(data_df, brand, category, from_year, to_year)
    return wordcloud(brand_df)


panel = (
    html.Div(
        html.Img(id="wordcloud-img"),
        className="panel",
    ),
)
