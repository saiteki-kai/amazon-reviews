import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.topics_barplot import topics_barplot
from dashboard.components.topics_sentiment_barplot import topics_sentiment_barplot
from dashboard.pages.products.components.item_list import item_list
from dashboard.pages.products.components.product_details import get_details
from dashboard.utils import update_brand


@dash.callback(
    Output({"type": "item", "asin": ALL}, "className"),
    Input({"type": "item", "asin": ALL}, "n_clicks"),
    Input({"type": "item", "asin": ALL}, "id"),
)
def set_active(product_clicks, product_ids):
    curr = dash.callback_context.triggered_id
    # print(curr)
    # print(product_clicks)

    if all([prod is None for prod in product_clicks]):
        return [""] * len(product_clicks)

    active = [False] * len(product_clicks)

    if curr is not None:
        active = [prod["asin"] == curr["asin"] for prod in product_ids]

    return ["active" if a else "" for a in active]


@dash.callback(
    Output("topics1", "figure"),
    Output("topics2", "figure"),
    Output("product-details", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("year-select", "value"),
    Input({"type": "item", "asin": ALL}, "n_clicks"),
)
def update_page(brand, category, year, product_ids):
    brand_df = update_brand(data_df, brand, category, year)

    selected_asin = None
    if not all([prod is None for prod in product_ids]):
        if "asin" in dash.callback_context.triggered_id:
            selected_asin = dash.callback_context.triggered_id["asin"]
            brand_df = brand_df[brand_df["asin"] == selected_asin]
            print("Selected ASIN:", selected_asin)

    fig1, order = topics_barplot(brand_df)
    fig2 = topics_sentiment_barplot(brand_df, order)

    details = get_details(selected_asin)

    return fig1, fig2, details


layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    item_list,
                    className="panel p-0",
                ),
                className="h-100",
                width=3,
            ),
            dbc.Col(
                [
                    html.Div(
                        html.Div(
                            id="product-details",
                            className="h-100",
                        ),
                        className="panel",
                    ),
                ],
                className="h-100",
                width=5,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                dcc.Graph(id="topics1"),
                                className="panel",
                            ),
                        ),
                        className="g-0 row-50",
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                dcc.Graph(id="topics2"),
                                className="panel",
                            ),
                        ),
                        className="g-0 row-50",
                    ),
                ],
                className="h-100",
                width=4,
            ),
        ],
        className="h-100 g-0",
    ),
    className="page-container",
)
