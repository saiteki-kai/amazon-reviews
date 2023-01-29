import dash
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.topics_barplot import topics_barplot
from dashboard.utils import update_brand


@dash.callback(
    Output("topics-distribution", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_topics(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)
    fig1, order = topics_barplot(brand_df)
    return fig1


panel = html.Div(
    dcc.Graph(id="topics-distribution", config={"displayModeBar": False}),
    className="panel",
)
