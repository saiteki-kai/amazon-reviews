import dash_bootstrap_components as dbc
from dash import html

layout = html.Div(
    dbc.Container(
        [
            html.H1("Products"),
        ],
        className="py-3",
    ),
)
