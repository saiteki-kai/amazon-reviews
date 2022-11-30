import dash_bootstrap_components as dbc
from dash import Dash

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css",  # noqa: E501
        "rel": "stylesheet",
    },
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
