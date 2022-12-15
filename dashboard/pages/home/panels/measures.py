import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

from dashboard.app import data_df

panel = html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H3("N. Products: 7.5K"),
                    html.H3("N. Reviews: 100K"),
                    html.H3("AVG rating: 4.7"),
                ],
            ),
            id="row6",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    figure=px.pie(
                        data_df["sentiment"].value_counts(),
                        values="sentiment",
                        color_discrete_sequence=["#f54242", "#27d957"],
                        names=["positive", "negative"],
                        hole=0.65,
                    )
                ),
                className="h-100",
            ),
            id="row7",
        ),
    ],
    className="panel",
)
