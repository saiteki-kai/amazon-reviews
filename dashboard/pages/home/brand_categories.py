import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc

from dashboard.app import data_df
from dashboard.utils import update_brand


@dash.callback(
    Output("brand-categories", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_brand_categories(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    category_count = brand_df["category"].value_counts().reset_index()
    category_count_df = (
        pd.DataFrame(category_count)
        .rename(columns={"category": "count", "index": "category"})
        .reset_index()
    )

    sentiments_count = brand_df.groupby("category")["sentiment"].value_counts()
    sentiments_count_perc = (
        sentiments_count / sentiments_count.groupby("category").sum() * 100
    )
    sentiments_df_perc = (
        pd.DataFrame(sentiments_count_perc)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    order = dict(category=list(brand_df["category"].value_counts().index))

    fig1 = px.bar(
        category_count_df,
        x="count",
        y="category",
        category_orders=order,
    )
    fig1.update_xaxes(showgrid=False, title_text="")
    fig1.update_yaxes(showgrid=False, title_text="")
    fig1.update_layout(margin=dict(l=0, t=0, r=0, b=0))

    fig2 = px.bar(
        sentiments_df_perc,
        x="count",
        y="category",
        color="sentiment",
        barmode="relative",
        category_orders=order,
    )
    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig2.update_layout(margin=dict(l=0, t=0, r=0, b=0))

    return dbc.Row(
        [
            dbc.Col(
                dbc.Row(
                    dcc.Graph(
                        figure=fig1,
                    )
                ),
            ),
            dbc.Col(dcc.Graph(figure=fig2)),
        ],
        id="row3",
    )
