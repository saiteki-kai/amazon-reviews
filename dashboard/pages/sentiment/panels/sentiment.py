import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

from dashboard.app import data_df
from dashboard.config import default_layout
from dashboard.utils import update_brand


@dash.callback(
    Output("sentiment-distribution", "figure"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
    Input("from-year-select", "value"),
    Input("to-year-select", "value"),
)
def update_sentiment(brand, category, from_year, to_year):
    brand_df = update_brand(data_df, brand, category, from_year, to_year)

    df = pd.DataFrame(brand_df["sentiment"].value_counts().reset_index())
    df = df.rename(columns={"index": "sentiment", "sentiment": "count"})
    df["sentiment"] = df["sentiment"].astype("category")

    fig = px.pie(
        df,
        names="sentiment",
        values="count",
        color_discrete_sequence=["#27d957", "#f54242"],
        hole=0.65,
        title="Sentiment",
    )
    fig.update_layout(default_layout)
    fig.update_layout(legend_title="sentiment")

    return fig


panel = html.Div(
    dcc.Graph(id="sentiment-distribution", config={"displayModeBar": False}),
    className="panel",
)
