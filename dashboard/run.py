from dash import html

from dashboard.app import app
from dashboard.layout import layout

app.layout = html.Div(
    id="container",
    className="fluid-container",
    children=layout,
)


if __name__ == "__main__":
    app.run_server(debug=True)
