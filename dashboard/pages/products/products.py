from math import floor

import dash
import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.components.reviews_rating import reviews_rating
from dashboard.components.sentiment_piechart import sentiment_piechart
from dashboard.components.topics_barplot import topics_barplot
from dashboard.components.topics_sentiment_barplot import topics_sentiment_barplot
from dashboard.utils import update_brand

tmp_id = "B00L64NSL2"


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
    Output("star_distribution", "figure"),
    Output("round", "figure"),
    Output("topics1", "figure"),
    Output("topics2", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("year-select", "value"),
    Input({"type": "item", "asin": ALL}, "n_clicks"),
)
def dynamic_page(brand, category, year, product_ids):
    brand_df = update_brand(data_df, brand, category, year)

    if not all([prod is None for prod in product_ids]):
        selected_asin = dash.callback_context.triggered_id["asin"]
        brand_df = brand_df[brand_df["asin"] == selected_asin]
        print("Selected ASIN:", selected_asin)

    fig1 = reviews_rating(brand_df)
    fig2 = sentiment_piechart(brand_df)
    fig3, order = topics_barplot(brand_df)
    fig4 = topics_sentiment_barplot(brand_df, order)

    return fig1, fig2, fig3, fig4


PAGE_SIZE = 5


def row_item(row):
    return dbc.ListGroupItem(
        row.title,
        id={"type": "item", "asin": row.asin},
        action=True,
        # active=True
    )


@dash.callback(
    Output("items", "children"),
    Output("pagination", "max_value"),
    Output("total", "children"),
    Input("pagination", "active_page"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("year-select", "value"),
)
def update_table(page, brand, category, year):
    brand_df = update_brand(data_df, brand, category, year)
    brand_df = brand_df.drop_duplicates(["asin"])

    if not page:
        page = 1

    page_idx = page - 1

    start = page_idx * PAGE_SIZE
    end = (page_idx + 1) * PAGE_SIZE

    total = floor(len(brand_df) / PAGE_SIZE)

    return (
        brand_df.iloc[start:end].apply(row_item, axis=1),
        total,
        f"Showing {PAGE_SIZE} items out of {total} results",
    )


item_list = html.Div(
    id="item-list",
    children=[
        dbc.CardBody(
            [
                dbc.ListGroup(id="items"),
            ],
        ),
        dbc.CardFooter(
            className="py-2 mx-2",
            children=[
                html.Small(
                    id="total",
                    className="text-muted",
                ),
                dbc.Pagination(
                    id="pagination",
                    max_value=0,
                    fully_expanded=False,
                    previous_next=True,
                ),
            ],
        ),
    ],
)

layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.Div(className="panel", children=item_list),
                className="h-100",
                width=4,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                id="star_distribution",
                                className="panel",
                            ),
                            className="row-50",
                        ),
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                dcc.Graph(id="round"),
                                className="panel",
                            )
                        ),
                        className="row-50",
                    ),
                ],
                className="h-100",
                width=4,
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

# @dash.callback(
#     Output("group_list", "children"),
#     Input("brand-select", "value"),
#     Input("category-select", "value"),
# )
# def update_plot(brand, category):
#     #update graph brand
#     brand_df = update_brand(data_df, brand, category)

#     element = []
#     for _, row in brand_df.iterrows():
#         element.append(dbc.ListGroupItem([
#             html.Div([
#                 html.Small(row.title),
#                 html.Small("Yay!", className="text-success"),
#             ]),
#             html.H5("ciao, seconda riga"),
#         ]))

#     return element

# table_header = html.Thead(
#     html.Tr(
#         [
#             html.Th("Text"),
#             html.Th("Vote", style={"width": "15%"}),
#             html.Th("Sentiment", style={"width": "15%"}),
#             html.Th("Topics", style={"width": "15%"}),
#         ],
#     ),
# )
