from math import ceil

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.utils import update_brand

PAGE_SIZE = 12


def row_item(row):
    return dbc.ListGroupItem(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.Img(src=row.imageURLHighRes),
                        className="item-img",
                    ),
                    width=3,
                    className="h-100",
                ),
                dbc.Col(
                    html.Span(row.title, className="item-title"),
                    className="h-100",
                ),
            ],
            className="item",
        ),
        id={"type": "item", "asin": row.asin},
        action=True,
        # active=True
    )


@dash.callback(
    Output("items", "children"),
    Output("pagination", "max_value"),
    # Output("total", "children"),
    Input("pagination", "active_page"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def update_table(page, brand, category, from_year, to_year):
    brand_df = update_brand(data_df, brand, category, from_year, to_year)
    brand_df = brand_df.drop_duplicates(["asin"])

    if not page:
        page = 1

    page_idx = page - 1

    start = page_idx * PAGE_SIZE
    end = (page_idx + 1) * PAGE_SIZE

    total = ceil(len(brand_df) / PAGE_SIZE)

    return (
        brand_df.iloc[start:end].apply(row_item, axis=1),
        total,
        # f"Showing {PAGE_SIZE} items out of {total} results",
    )


item_list = html.Div(
    id="item-list",
    children=[
        html.Div(
            [
                dbc.ListGroup(id="items"),
            ],
            id="item-list-body",
        ),
        html.Div(
            id="item-list-footer",
            # className="py-2 mx-2",
            children=[
                # html.Small(
                #     id="total",
                #     className="text-muted",
                # ),
                dbc.Pagination(
                    id="pagination",
                    max_value=0,
                    fully_expanded=False,
                    previous_next=True,
                    size="sm",
                ),
            ],
        ),
    ],
)
