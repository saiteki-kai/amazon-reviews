import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

# from dashboard.app import data_df
# from dashboard.utils import update_brand

layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.ListGroup(id="group_list"),
                    className="panel",
                ),
                className="h-100",
                width=4,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(className="panel"),
                                className="h-100",
                            ),
                            dbc.Col(
                                html.Div(className="panel"),
                                className="h-100",
                            ),
                            dbc.Col(
                                html.Div(className="panel"),
                                className="h-100",
                            ),
                        ],
                        id="row1",
                        className="g-0",
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(className="panel"),
                            className="h-100",
                        ),
                        id="row2",
                        className="g-0",
                    ),
                ],
                className="h-100",
                width=8,
            ),
        ],
        className="h-100 g-0",
    ),
    className="page-container",
)


@dash.callback(
    Output("group_list", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_plot(brand, category):
    # update graph brand
    # brand_df = update_brand(data_df, brand, category)
    pass

    # dbc.ListGroup(
