from dash import html

from dashboard.app import app
from dashboard.components.item_list import item_list

app.layout = html.Div(
    id="container",
    className="fluid-container",
    children=item_list,
)


if __name__ == "__main__":
    app.run_server(debug=True)
