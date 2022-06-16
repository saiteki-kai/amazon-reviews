import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

from reviews.config import processed_data_dir

reviews_df = pd.read_json(
    processed_data_dir / "reviews_digital_cameras.json.gz", orient="records"
)
reviews_df = reviews_df.sample(10)

table_header = html.Thead(
    html.Tr(
        [
            html.Th("Text"),
            html.Th("Vote", style={"width": "120px"}),
            html.Th("Sentiment", style={"width": "10%"}),
            html.Th("Topics", style={"width": "10%"}),
        ],
    ),
)


def vote(stars):
    return html.Div(
        [
            html.I(className=f"bi bi-star{'-fill' if i < stars else ''}")
            for i in range(5)
        ]
    )


def row_item(row):
    return html.Tr(
        [
            html.Td(row["text"]),
            html.Td(vote(row["overall"])),
            html.Td("Positive"),
            html.Td(
                [
                    dbc.Badge("Topic 1", className="me-1"),
                    dbc.Badge("Topic 2", className="me-1"),
                ],
            ),
        ],
    )


table_body = html.Tbody(reviews_df.apply(row_item, axis=1))

item_list = html.Div(
    id="item-list",
    className="col-12",
    children=[
        dbc.Table(
            children=[
                table_header,
                table_body,
            ],
        ),
    ],
)
