from collections import Counter

import pandas as pd
import plotly.express as px

from dashboard.utils import default_layout


def topics_sentiment_barplot(brand_df, order):
    pos_count = Counter()
    neg_count = Counter()

    for t in brand_df["topics"].values:
        pos_topics = set([f"{s['name']}" for s in t if s["sentiment"] == 0])
        neg_topics = set([f"{s['name']}" for s in t if s["sentiment"] == 1])

        pos_count.update(pos_topics)
        neg_count.update(neg_topics)

    pos_df = pd.DataFrame(pos_count.items(), columns=["topic", "positive"])
    neg_df = pd.DataFrame(neg_count.items(), columns=["topic", "negative"])

    st_counts = pd.merge(pos_df, neg_df, on="topic")
    st_counts["topic"] = st_counts["topic"].astype("category")

    total = st_counts["positive"] + st_counts["negative"]
    st_counts["positive"] = st_counts["positive"] / total * 100
    st_counts["negative"] = st_counts["negative"] / total * 100

    st_counts.set_index("topic", inplace=True)
    st_counts.sort_index(inplace=True)
    # st_counts = st_counts.iloc[[(o) for o in order][::-1]]

    df_senti = (
        st_counts.stack(level=0)
        .reset_index()
        .rename(columns={"level_1": "sentiment", 0: "count"})
    )

    category_orders = {"sentiment": ["positive", "negative"]}

    fig = px.bar(
        df_senti,
        y="topic",
        x="count",
        color="sentiment",
        color_discrete_sequence=["#27d957", "#f54242"],
        barmode="relative",
        category_orders=category_orders,
        title="Sentiment By Topic",
    )
    fig.update_layout(default_layout)
    fig.update_xaxes(ticksuffix="%")

    return fig
