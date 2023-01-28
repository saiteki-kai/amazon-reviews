from collections import Counter

import pandas as pd
import plotly.express as px


def topics_sentiment_barplot(brand_df, order):
    pos_count = Counter()
    neg_count = Counter()

    for t in brand_df["topics"].values:
        pos_topics = set([f"{s['name']}" for s in t if s["sentiment"] == 0])
        neg_topics = set([f"{s['name']}" for s in t if s["sentiment"] == 1])

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
    # st_counts = st_counts.iloc[[(o) for o in order][::-1]]

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
    fig2.update_layout({"margin": dict(l=0, t=0, r=0, b=0)})
    return fig2
