import dash_bootstrap_components as dbc
from dash import html

from dashboard.app import data_df

# Brand Select
brand_select = dbc.Select(
    id="brand-select",
    options=[
        {"label": brand, "value": brand}
        for brand in list(data_df["brand"].value_counts().index)
    ],
    value="corsair",
    class_name="mr-2",
)

# Brand Categories Select
category_select = dbc.Select(
    id="category-select",
    options=[],
)

layout = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        children=[
                            dbc.NavLink(
                                "Home",
                                href="/",
                                active="exact",
                                className="navbar-dark",
                            ),
                            dbc.NavLink(
                                "Products",
                                href="/details",
                                active="exact",
                                className="navbar-dark",
                            ),
                            dbc.NavLink(
                                "Comparison",
                                href="/comparison",
                                active="exact",
                                className="navbar-dark",
                            ),
                        ],
                    ),
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [html.Span("Brand"), brand_select],
                                    className="select-container",
                                ),
                                width=7,
                            ),
                            dbc.Col(
                                html.Div(
                                    [html.Span("Category"), category_select],
                                    className="select-container",
                                ),
                                width=5,
                            ),
                        ],
                        justify="between",
                    ),
                    width=4,
                ),
            ],
            justify="between",
            class_name="w-100",
        ),
        fluid=True,
    ),
    dark=True,
    color="primary",
)
