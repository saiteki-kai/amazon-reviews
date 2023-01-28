import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.topics_barplot import topics_barplot
from dashboard.components.topics_sentiment_barplot import topics_sentiment_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("topics-distribution", "figure"),
    Output("topics-distribution-perc", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_topics_sentiment(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    fig1, order = topics_barplot(brand_df)
    fig2 = topics_sentiment_barplot(brand_df, order)
    return fig1, fig2


panel = html.Div(
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id="topics-distribution"),
                className="h-100",
            ),
            dbc.Col(
                dcc.Graph(id="topics-distribution-perc"),
                className="h-100",
            ),
        ],
        className="h-100",
    ),
    className="panel",
)
