import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.app import data_df
from dashboard.components.sentiment_piechart import sentiment_piechart

panel = html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H6("N. products: 7.5K"),
                    html.H6("N. Reviews: 100K"),
                    html.H6("AVG rating: 4.7"),
                ],
            ),
            id="row6",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(figure=sentiment_piechart(data_df)),
                className="h-100",
            ),
            id="row7",
        ),
    ],
    className="panel",
)
