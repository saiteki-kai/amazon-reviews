from collections import Counter
from math import floor

import dash
import dash_bootstrap_components as dbc
import humanize
import numpy as np
import pandas as pd
import plotly.express as px
from dash import ALL, Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.utils import update_brand


def star_row(df, n):
    n_reviews = len(df[df["overall"] == n])

    if n_reviews == 0:
        return "0"

    overall_perc = n_reviews / len(df) * 100
    stars_icon = [html.I(className="fa-solid fa-star") for _ in range(n)]

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Small(
                            f"{overall_perc:.1f}%\
                             - {humanize.intcomma(n_reviews)} Reviews",
                            className="m-0",
                        )
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
    Output("star_distribution", "children"),
    Output("round", "figure"),
    Output("topics1", "figure"),
    Output("topics2", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input({"type": "item", "asin": ALL}, "n_clicks"),
)
def dynamic_page(brand, category, product_ids):
    brand_df = update_brand(data_df, brand, category)

    if not all([prod is None for prod in product_ids]):
        selected_asin = dash.callback_context.triggered_id["asin"]
        # brand_df = brand_df[brand_df["asin"] == selected_asin]
        print("Selected ASIN:", selected_asin)

    # star distribution
    star = [star_row(brand_df, i) for i in range(5, 0, -1)]

    # round
    fig = px.pie(
        brand_df["sentiment"].value_counts(),
        values="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        names=["positive", "negative"],
        hole=0.65,
    )

    # topics
    count = Counter()
    for x in brand_df["topics"].values:
        topics = set(["T" + str(y["topic"]) for y in x])
        count.update(topics)

    topics_count = pd.DataFrame(count.items(), columns=["topic", "count"])
    # topics_count["topic"] = topics_count["topic"].astype("category")

    order = topics_count.sort_values(by="count", ascending=False)
    order = order.reset_index()["topic"]

    fig1 = px.bar(
        topics_count,
        y="topic",
        x="count",
        color_discrete_sequence=["#108de4"],
        category_orders=dict(topic=order),
    )
    fig1.update_xaxes(showgrid=False, title_text="")
    fig1.update_yaxes(showgrid=False, title_text="")
    fig1.update_layout({"margin": dict(l=0, t=0, r=0, b=0)})

    pos_count = Counter()
    neg_count = Counter()

    for t in brand_df["topics"].values:
        pos_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 0])
        neg_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 1])

        pos_count.update(pos_topics)
        neg_count.update(neg_topics)

    pos_df = pd.DataFrame(pos_count.items(), columns=["topic", "pos"])
    neg_df = pd.DataFrame(neg_count.items(), columns=["topic", "neg"])

    st_counts = pd.merge(pos_df, neg_df, on="topic")
    st_counts["topic"] = st_counts["topic"].astype("category")

    total = st_counts["pos"] + st_counts["neg"]
    st_counts["pos"] = st_counts["pos"] / total * 100
    st_counts["neg"] = st_counts["neg"] / total * 100

    st_counts.set_index("topic", inplace=True)
    st_counts.sort_index(inplace=True)
    st_counts = st_counts.iloc[[int(o[1:]) for o in order][::-1]]

    df_senti = (
        st_counts.stack(level=0)
        .reset_index()
        .rename(columns={"level_1": "sentiment", 0: "count"})
    )

    fig2 = px.bar(
        df_senti,
        y="topic",
        x="count",
        color="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        barmode="relative",
        category_orders=dict(topic=order),
    )

    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="")
    fig2.update_layout({"margin": dict(l=0, t=0, r=0, b=0)})

    return star, fig, fig1, fig2


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
)
def update_table(page, brand, category):
    brand_df = update_brand(data_df, brand, category)
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
                html.Div(
                    [
                        html.Div(id="star_distribution"),
                        html.Div(
                            dcc.Graph(id="round"),
                        ),
                    ],
                    className="panel",
                ),
                className="h-100",
            ),
            dbc.Col(
                [
                    dbc.Row(
                        html.Div(
                            [
                                html.Div(dcc.Graph(id="topics1")),
                            ],
                            className="panel",
                        ),
                        className="h-50",
                    ),
                    dbc.Row(
                        html.Div(
                            [
                                html.Div(dcc.Graph(id="topics2")),
                            ],
                            className="panel",
                        ),
                        className="h-50",
                    ),
                ],
                className="h-100",
                # width=8,
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
