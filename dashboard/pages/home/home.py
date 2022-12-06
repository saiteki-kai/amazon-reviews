import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, dcc, html

import dashboard.pages.home.brand_categories  # noqa:F401
import dashboard.pages.home.reviews_sentiment  # noqa:F401
import dashboard.pages.home.star_distribution  # noqa:F401
import dashboard.pages.home.topics_sentiment  # noqa:F401
import dashboard.pages.home.word_cloud  # noqa:F401
from dashboard.app import data_df
from dashboard.pages.home.sentiment_over_time import sentiment_over_time


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
                    dbc.Col(html.H2("Measures"), width=2),
                    dbc.Col(id="star-distribution", width=2),
                    dbc.Col(
                        dcc.Graph(
                            figure=px.pie(
                                data_df["sentiment"].value_counts(),
                                values="sentiment",
                                names=["positive", "negative"],
                                hole=0.65,
                            )
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Div(id="brand-categories"),
                            html.Div(id="topics-sentiment"),
                        ],
                        width=6,
                    ),
                ],
                id="row1",
            ),
            dbc.Row(
                [
                    dbc.Col(sentiment_over_time, width=6),
                    dbc.Col(html.Img(id="wordcloud"), width=6),
                ],
                id="row2",
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="page-container", 
)
