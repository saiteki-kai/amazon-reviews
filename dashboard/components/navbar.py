import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

from dashboard.app import data_df

# Brand Select
brand_select = dbc.Select(
    id="brand-select",
    options=[{"label": brand, "value": brand} for brand in list(data_df["brand"].unique())],
    value="corsair",
    size="sm",
)

# Brand Categories Select
category_select = dbc.Select(
    id="category-select",
    options=[],
    size="sm",
)

years = sorted(list(data_df["timestamp"].dt.year.unique()))[::-1]
from_year_select = dbc.Select(
    id="from-year-select",
    options=[{"label": year, "value": year} for year in years],
    value=str(years[-1]),
    size="sm",
)

to_year_select = dbc.Select(
    id="to-year-select",
    options=[{"label": year, "value": year} for year in years],
    value=str(years[0]),
    size="sm",
)


@dash.callback(
    Output("category-select", "options"),
    Output("category-select", "value"),
    Input("brand-select", "value"),
    Input("url", "pathname"),
)
def update_categories(brand, pathname):
    df = data_df[data_df["brand"] == brand]

    categories = list(df["category"].value_counts().index)
    options = [{"label": c, "value": c} for c in categories]

    if pathname == "/comparison":
        return options, options[0]["value"]

    options = [{"label": "All", "value": "All"}] + options

    return options, "All"


@dash.callback(
    Output("from-year-select", "options"),
    Output("from-year-select", "value"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_from_year(brand, category):
    df = data_df[(data_df["brand"] == brand)].copy()

    if category != "All":
        df = df[df["category"] == category].copy()

    years = sorted(list(df["timestamp"].dt.year.unique()))[::-1]
    options = [{"label": year, "value": year} for year in years]

    return options, str(options[-1]["label"])


@dash.callback(
    Output("to-year-select", "options"),
    Input("from-year-select", "value"),
)
def update_to_year(from_year):
    return [{"label": year, "value": year} for year in years if year >= int(from_year)]


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
                                "Sentiment",
                                href="/sentiment",
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
                    width=4,
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [html.Span("Brand"), brand_select],
                                    className="select-container",
                                ),
                            ),
                            dbc.Col(
                                html.Div(
                                    [html.Span("Category"), category_select],
                                    className="select-container",
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Span("Period"),
                                        html.Div(
                                            [
                                                from_year_select,
                                                to_year_select,
                                            ],
                                            className="year-selector",
                                        ),
                                    ],
                                    className="select-container",
                                ),
                            ),
                        ],
                        justify="between",
                        className="selects g-0",
                    ),
                    width=8,
                ),
            ],
            align="center",
            justify="between",
            className="w-100 g-0",
        ),
        fluid=True,
    ),
    dark=True,
    color="primary",
)
