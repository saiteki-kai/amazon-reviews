import dash_bootstrap_components as dbc
from dash import Dash, html

from dashboard.components.item_list import item_list

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css",  # noqa: E501
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    id="container",
    className="fluid-container",
    children=item_list,
)


if __name__ == "__main__":
    app.run_server(debug=True)
