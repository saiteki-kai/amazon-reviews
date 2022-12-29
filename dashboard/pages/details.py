from math import floor
import dash
import humanize
import numpy as np
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc

from dashboard.app import data_df
from dashboard.utils import update_brand

def star_row(df, n):
    n_reviews = len(df[df["overall"] == n])

    overall_perc = n_reviews / len(df) * 100
    stars_icon = [html.I(className="fa-solid fa-star") for _ in range(n)]

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Small(f"{overall_perc:.1f}% - {humanize.intcomma(n_reviews)} Reviews", className="m-0")
                    ),
                    dbc.Col(
                        stars_icon,
                        style={"textAlign": "right"},
                    ),
                ]
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Progress(
                        value=np.round(overall_perc),
                        color="#108de4",
                        style={"height": "8px"},
                    ),
                ),
            ),
        ],
    )

tmp_id = "B00L64NSL2"

@dash.callback(
    Output("star_distribution", "children"),
    Output("round", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def dynamic_page(brand, category):
    brand_df = update_brand(data_df, brand, category)
    brand_df = brand_df[brand_df["asin"] == tmp_id]

    #star distrubution
    star = [star_row(brand_df, i) for i in range(5, 0, -1)]

    #round
    fig=px.pie(
            brand_df["sentiment"].value_counts(),
            values="sentiment",
            color_discrete_sequence=["#f54242", "#27d957"],
            names=["positive", "negative"],
            hole=0.65,
        )

    return star, fig






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
                html.Div([ 
                    html.Div(id="star_distribution"), 
                    html.Div(
                        dcc.Graph( id = "round"),
                    ),                                                                     
                    ], className="panel",),
                    className="h-100",
            ),
            dbc.Col(
                [
                    dbc.Row(
                        html.Div([
                            html.Div(id="topic1"),
                        ], className="panel",),
                        className="h-50",
                    ),
                    dbc.Row(
                        html.Div([
                            html.Div(id="topic2"),
                        ], className="panel",),
                        className="h-50",
                    )
                ],
                className="h-100",
               #width=8,
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