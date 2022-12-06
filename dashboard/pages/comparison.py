import datetime
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html
from reviews.config import processed_data_dir
import pandas as pd
import plotly.express as px

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "global_sentiment")
                    ]),
                    dbc.Col([
                        dcc.Dropdown(id = "topic_dropdown",
                            placeholder = "select topic",
                            value = 'Gold',
                            clearable = False,
                    ),
                        dcc.Graph(id = "topic_sentiment")
                    ]),
                ],id = "row4",),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id = "time_brand_pos_sentiment")
                    ]),
                    dbc.Col([
                        dcc.Graph(id = "time_brand_neg_sentiment")
                    ]),
                ],id = "row5",),
            ],
            fluid=True,
            className="py-3",
        )
    ],
    className="page-container",
)

# function for dynamic dash page -----------------------------------------------
from dashboard.app import data_df
from dashboard.utils import update_brand
import dash

@dash.callback(
    Output("global_sentiment", "figure"),
    Output("time_brand_pos_sentiment", "figure"),
    Output("time_brand_neg_sentiment", "figure"),
    Output("topic_sentiment", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)

def update_plot(brand, category):
    if(category == "All"):
        dash.no_update

    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    category_df = data_df[data_df["category"] == category]
    category_df = category_df[category_df["brand"] != brand]

    # competitors
    competitors = list(category_df["brand"].value_counts().index)[:5] + [brand]

    competitors_df = data_df[data_df["brand"].isin(competitors)]
    
    # gloabl sentiment 
    sentiment_df = competitors_df.groupby("brand")["sentiment"].value_counts()
    sentiment_df_perc = (
        sentiment_df / sentiment_df.groupby("brand").sum() * 100
    )    
    sentiment_df_perc = (
        pd.DataFrame(sentiment_df_perc)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )
    
    fig2 = px.bar(
        sentiment_df_perc,
        x="brand",
        y="count",
        color="sentiment",
        barmode="relative",
        category_orders=dict(brand = [brand, *competitors]),
    )
    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig2.update_layout(margin=dict(l=0, t=0, r=0, b=0))

    # positive sentiment in time
    sentiments_count = competitors_df[competitors_df["sentiment"] == "positive"].groupby(["timestamp", "brand"])["sentiment"].value_counts()
    sentiments_df = (
        pd.DataFrame(sentiments_count)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig3 = px.line(
        sentiments_df,
        x="timestamp",
        y="count",
        color="brand",
        #title="Sentiment Over Time",
    )
    fig3.update_xaxes(
        showgrid=False,
        title_text="",
        # range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig3.update_yaxes(showgrid=False, title_text="# Reviews")
    fig3.update_layout({"margin": dict(l=0, r=0, b=0)})

    # negative sentiment in time 
    sentiments_count = competitors_df[competitors_df["sentiment"] == "negative"].groupby(["timestamp", "brand"])["sentiment"].value_counts()
    sentiments_df = (
        pd.DataFrame(sentiments_count)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )

    fig4 = px.line(
        sentiments_df,
        x="timestamp",
        y="count",
        color="brand",
        #title="Sentiment Over Time",
    )
    fig4.update_xaxes(
        showgrid=False,
        title_text="",
        # range=list(map(lambda x: datetime.datetime(x, 1, 1), years)),
    )
    fig4.update_yaxes(showgrid=False, title_text="# Reviews")
    fig4.update_layout({"margin": dict(l=0, r=0, b=0)})

    # sentimenti for topic
    fig5 = px.bar(
        sentiment_df_perc,
        x="brand",
        y="count",
        color="sentiment",
        barmode="relative",
        category_orders=dict(brand = [brand, *competitors]),
    )
    fig5.update_xaxes(showgrid=False, title_text="")
    fig5.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig5.update_layout(margin=dict(l=0, t=0, r=0, b=0))

    return fig2, fig3, fig4, fig5