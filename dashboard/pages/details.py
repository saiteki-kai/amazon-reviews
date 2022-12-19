from math import floor
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.utils import update_brand


PAGE_SIZE = 5

def row_item(row):
    print(row.asin)
    return dbc.ListGroupItem(
        row.title,
        id=row.asin,
        n_clicks=0,
        action=True
    )

@dash.callback(
    Output("primo", "children"),
    Input("B000234UPQ", "n_click"),
    prevent_initial_call=True
)
def click_list(n):
    print(n)
    return html.Small("ciao")

@dash.callback(
    Output("items", "children"),
    Output("pagination", "max_value"),
    Output("total", "children"),
    Input("pagination", "active_page"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_table(page, brand, category):
    brand_df = update_brand(data_df, brand, category)
    brand_df = brand_df.drop_duplicates(["asin"])

    if not page:
        page = 1

    page_idx = page - 1

    start = page_idx * PAGE_SIZE
    end = (page_idx + 1) * PAGE_SIZE

    total = floor(len(brand_df)/PAGE_SIZE)

    return brand_df.iloc[start:end].apply(row_item, axis=1), total, f"Showing {PAGE_SIZE} items out of {total} results"

table_body = dbc.ListGroup(
    id="items",
)

item_list = html.Div(
    id="item-list",
    children=[
        dbc.CardBody(                    
            table_body
        ),
        dbc.CardFooter(
            className="py-2 mx-2",
            children=[
                html.Small(
                    id = "total",
                    className="text-muted",
                ),
                dbc.Pagination(
                    id="pagination",
                    max_value = 0,
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
                html.Div(
                    className="panel",
                    children = item_list
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
                                id="primo",
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