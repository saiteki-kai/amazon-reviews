import dash
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.topics_barplot import topics_barplot
from dashboard.components.topics_sentiment_barplot import topics_sentiment_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("topics-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_topics_sentiment(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    _, order = topics_barplot(brand_df)
    fig = topics_sentiment_barplot(brand_df, order)

    return fig


panel = html.Div(
    dcc.Graph(id="topics-distribution-perc", config={"displayModeBar": False}),
    className="panel",
)
