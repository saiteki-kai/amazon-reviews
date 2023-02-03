import pandas as pd
import plotly.express as px

from dashboard.utils import default_layout


def category_sentiment_barplot(brand_df, order):
    sentiments_count = brand_df.groupby("category")["sentiment"].value_counts()
    sentiments_count_perc = (
        sentiments_count / sentiments_count.groupby("category").sum() * 100
    )
    sentiments_df_perc = (
        pd.DataFrame(sentiments_count_perc)
        .rename(columns={"sentiment": "percentage"})
        .reset_index()
    )
    category_orders = {"sentiment": ["positive", "negative"]}

    fig = px.bar(
        sentiments_df_perc,
        x="percentage",
        y="category",
        color="sentiment",
        color_discrete_sequence=["#27d957", "#f54242"],
        barmode="relative",
        category_orders=category_orders,
        title="Sentiment By Category",
    )

    fig.update_layout(default_layout)
    fig.update_xaxes(ticksuffix="%")

    return fig
