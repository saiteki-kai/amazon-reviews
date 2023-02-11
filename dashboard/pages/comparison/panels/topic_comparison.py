from collections import Counter

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def sentiment_aspect_df(reviews_df):
    pos_count = Counter()
    neg_count = Counter()

    for t in reviews_df["topics"].values:
        pos_topics = set([s["name"] for s in t if s["sentiment"] == 0])
        neg_topics = set([s["name"] for s in t if s["sentiment"] == 1])

        pos_count.update(pos_topics)
        neg_count.update(neg_topics)

    pos_df = pd.DataFrame(pos_count.items(), columns=["topic", "pos"])
    neg_df = pd.DataFrame(neg_count.items(), columns=["topic", "neg"])

    pos_df = pd.DataFrame(pos_df.groupby("topic")["pos"].sum()).reset_index()
    neg_df = pd.DataFrame(neg_df.groupby("topic")["neg"].sum()).reset_index()

    st_counts = pd.merge(pos_df, neg_df, on="topic")
    st_counts["topic"] = st_counts["topic"].astype("category")

    total = st_counts["pos"] + st_counts["neg"]
    st_counts["pos"] = st_counts["pos"] / total * 100
    st_counts["neg"] = st_counts["neg"] / total * 100

    st_counts.set_index("topic", inplace=True)
    st_counts.sort_index(inplace=True)

    df_senti = st_counts.stack(level=0).reset_index().rename(columns={"level_1": "sentiment", 0: "count"})

    return df_senti


def get_topics_score_by_brand(brand_competitor, competitors_df, topics, sentiment_selected):
    df2 = competitors_df[competitors_df["brand"] == brand_competitor].copy()
    df2 = sentiment_aspect_df(df2)
    df2 = df2[df2["topic"].isin(topics)].copy()

    df2["topic"] = df2["topic"].astype(pd.CategoricalDtype(set(topics), ordered=True))
    df2["count"] = df2["count"].astype(int)

    # sentiment_selected is 'positive' or 'negative'
    # but df2 contains 'pos' or 'neg' so sentiment_selected[:3]
    df2 = df2[df2["sentiment"] == sentiment_selected[:3]]

    return df2


def topic_comparison(competitors_df, competitor, color, topics, sentiment_selected):
    topics_count_df = get_topics_score_by_brand(competitor, competitors_df, topics, sentiment_selected)

    values = list(np.zeros(len(topics)))
    for _, row in topics_count_df.iterrows():
        values[topics.index(row["topic"])] = row["count"]
        values = pd.Series(values).replace(0, np.NAN).to_list()

    if len(values) > 0:
        values.append(values[0])

    if len(topics) > 0:
        topics.append(topics[0])

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=topics,
            fill="toself",
            connectgaps=True,
            fillcolor=color,
            line_color=color,
            mode=None,
            name=competitor,
        )
    )

    # fig.update_layout(default_layout)
    fig.update_layout(polar=dict(radialaxis_range=[0, 100]), margin=dict(t=60, b=60), title={"text": competitor})

    return fig
