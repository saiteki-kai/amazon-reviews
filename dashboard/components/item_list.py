from math import floor

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html

from dashboard.app import app
from reviews.config import asum_output_dir

PAGE_SIZE = 50

reviews_df = pd.read_json(asum_output_dir / "topics.json", orient="records")
reviews_df = reviews_df[:1000]


def vote(stars):
    return html.Div([html.I(className=f"bi bi-star{'-fill' if i < stars else ''}") for i in range(5)])


def topic_badge(topic):
    return dbc.Badge(
        f"Topic {topic['topic'] + 1}",
        className="me-1",
        color="green" if topic["sentiment"] == 0 else "red",
    )


def row_item(row):
    return html.Tr(
        [
            html.Td(row["text"]),
            html.Td(vote(row["overall"])),
            html.Td(str(row["sentiment"]).capitalize()),
            html.Td(list(map(topic_badge, row["topics"]))),
        ],
    )


@app.callback(
    Output("filtered-data", "data"),
    Input("search", "value"),
)
def filter_data(query):
    filtered_df = reviews_df

    if query is str and query != "":
        cond = reviews_df["text"].str.contains(query)
        filtered_df = reviews_df.loc[cond]

    return filtered_df.to_json(orient="records")


@app.callback(
    Output("footer", "children"),
    Input("filtered-data", "data"),
)
def footer(filtered_df):
    filtered_df = pd.read_json(filtered_df, orient="records")
    total = len(filtered_df)

    return [
        html.Small(
            f"Showing {PAGE_SIZE} items out of {total} results",
            className="text-muted",
        ),
        dbc.Pagination(
            id="pagination",
            max_value=floor(total / PAGE_SIZE),
            fully_expanded=False,
            previous_next=True,
        ),
    ]


@app.callback(
    Output("items", "children"),
    [
        Input("pagination", "active_page"),
        Input("filtered-data", "data"),
    ],
)
def update_table(page, filtered_df):
    if not page:
        page = 1

    page_idx = page - 1

    start = page_idx * PAGE_SIZE
    end = (page_idx + 1) * PAGE_SIZE

    filtered_df = pd.read_json(filtered_df, orient="records")
    return list(filtered_df.iloc[start:end].apply(row_item, axis=1))


table_header = html.Thead(
    html.Tr(
        [
            html.Th("Text"),
            html.Th("Vote", style={"width": "15%"}),
            html.Th("Sentiment", style={"width": "15%"}),
            html.Th("Topics", style={"width": "15%"}),
        ],
    ),
)

table_body = html.Tbody(
    id="items",
)


item_list = html.Div(
    id="item-list",
    className="col-9",
    children=[
        dcc.Store(id="filtered-data"),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H6("Reviews", className="m-2"),
                        dbc.Input(id="search", placeholder="Search products...", type="text"),
                    ],
                ),
                dbc.CardBody(
                    children=[
                        dbc.Table(
                            children=[
                                table_header,
                                table_body,
                            ],
                        ),
                    ],
                ),
                dbc.CardFooter(
                    id="footer",
                    className="py-2 mx-2",
                ),
            ],
        ),
    ],
)
