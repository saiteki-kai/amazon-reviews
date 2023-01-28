import pandas as pd
import plotly.express as px


def category_sentiment_barplot(brand_df, order):
    sentiments_count = brand_df.groupby("category")["sentiment"].value_counts()
    sentiments_count_perc = (
        sentiments_count / sentiments_count.groupby("category").sum() * 100
    )
    sentiments_df_perc = (
        pd.DataFrame(sentiments_count_perc)
        .rename(columns={"sentiment": "count"})
        .reset_index()
    )
    fig2 = px.bar(
        sentiments_df_perc,
        x="count",
        y="category",
        color="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        barmode="relative",
        category_orders=order,
    )
    fig2.update_xaxes(showgrid=False, title_text="")
    fig2.update_yaxes(showgrid=False, title_text="", showticklabels=False)
    fig2.update_layout(margin=dict(l=0, t=0, r=0, b=0))
    return fig2
