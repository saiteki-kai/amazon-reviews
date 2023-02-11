from math import floor

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html

from dashboard.app import data_df
from dashboard.pages.products.components.product_details import stars_icon
from dashboard.utils import update_brand

PAGE_SIZE = 4


def row_item(row):
    return dbc.ListGroupItem(
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(stars_icon(row.overall)),
                        dbc.Col(
                            dbc.Badge(
                                row.sentiment,
                                style={"color": "red" if row.sentiment == "negative" else "green"},
                                color="light",
                            ),
                            align="end",
                            className="sentiment",
                        ),
                    ],
                    justify="between",
                ),
                html.Div(
                    html.Span(row.summary, className="review-title"),
                ),
                html.Div(
                    html.Span(row.text, className="review-title"),
                ),
                html.Div(
                    [
                        dbc.Badge(
                            t["name"],
                            color="red" if t["sentiment"] == 1 else "green",
                            pill=True,
                            className="me-1",
                        )
                        for t in row.topics
                    ]
                ),
            ],
            className="review-item",
        ),
    )


@dash.callback(
    Output("review-items", "children"),
    Output("review-pagination", "max_value"),
    Input("review-pagination", "active_page"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
    Input("current-asin", "data"),
)
def update_table(page, brand, category, from_year, to_year, asin):
    brand_df = update_brand(data_df, brand, category, from_year, to_year)

    if asin is None:
        return None, 0

    reviews_df = brand_df[brand_df["asin"] == asin]

    if not page:
        page = 1

    page_idx = page - 1

    start = page_idx * PAGE_SIZE
    end = (page_idx + 1) * PAGE_SIZE

    total = floor(len(reviews_df) / PAGE_SIZE)

    return (
        reviews_df.iloc[start:end].apply(row_item, axis=1),
        total,
    )


review_list = html.Div(
    id="review-list",
    children=[
        html.Div(
            [
                dbc.ListGroup(id="review-items"),
            ],
            id="review-list-body",
        ),
        html.Div(
            id="review-list-footer",
            children=[
                dbc.Pagination(
                    id="review-pagination",
                    max_value=0,
                    fully_expanded=False,
                    previous_next=True,
                    size="sm",
                ),
            ],
        ),
    ],
)
