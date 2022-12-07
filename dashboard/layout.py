from dash import Input, Output, callback, dcc, html

from dashboard.components import navbar
from dashboard.pages import comparison, details
from dashboard.pages.home import home

layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar.layout,
        html.Div(id="page-content"),
    ]
)


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/details":
        return details.layout
    elif pathname == "/comparison":
        return comparison.layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
