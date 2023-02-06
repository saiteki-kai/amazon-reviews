from collections import Counter
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dashboard.utils import primary_color, secondary_color, default_layout



def sentiment_aspect_df(reviews_df):
    topic_mapping = {
        "T0": "psu",
        "T1": "time",
        "T2": "delivery",
        "T3": "cooling system",
        "T4": "cooling system",
        "T5": "performance",
        "T6": "memory",
        "T7": "satisfaction/recommanded",
        "T8": "psu",
        "T9": "price",
        "T10": "pc",  # mac, macbook, imac
        "T11": "video",
        "T12": "performance",
        "T13": "?",
        "T14": "buy",  # purchase
        "T15": "cooling system",  # (air flow)
        "T16": "cooling system",  # (temp)
        "T17": "overclocking",
        "T18": "satisfaction/recommanded",
        "T19": "installation",
        "T20": "satisfaction/recommanded",
        "T21": "buy",  # or satisfaction/recommanded
        "T22": "sound",
        "T23": "psu",
        "T24": "cooling system",  # (air flow)
        "T25": "quality",
        "T26": "satisfaction/recommanded",  # quality
        "T27": "delivery",
        "T28": "aesthetic",
        "T29": "performance",  # gaming
        "T30": "installation",
        "T31": "pc",  # (pc build / replacement / upgrade)
        "T32": "storage connectivity",
        "T33": "processor",
        "T34": "upgrade",
        "T35": "satisfaction/recommanded",
        "T36": "motherboard",
        "T37": "?",
        "T38": "cooling system",  # (air flow)
        "T39": "installation",
        "T40": "?",
        "T41": "motherboard",
        "T42": "cooling system",
        "T43": "optical disc",
        "T44": "memory",
        "T45": "temperature",  # cooling
        "T46": "satisfaction/recommanded",
        "T47": "satisfaction/recommanded",
        "T48": "motherboard",
        "T49": "memory",
    }

    pos_count = Counter()
    neg_count = Counter()

    for t in reviews_df["topics"].values:
        pos_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 0])
        neg_topics = set([f"T{s['topic']}" for s in t if s["sentiment"] == 1])

        pos_count.update(pos_topics)
        neg_count.update(neg_topics)

    pos_df = pd.DataFrame(pos_count.items(), columns=["topic", "pos"])
    neg_df = pd.DataFrame(neg_count.items(), columns=["topic", "neg"])

    pos_df["topic"] = pos_df["topic"].apply(lambda x: topic_mapping[x]).astype("category")
    pos_df = pd.DataFrame(pos_df.groupby("topic")["pos"].sum()).reset_index()

    neg_df["topic"] = neg_df["topic"].apply(lambda x: topic_mapping[x]).astype("category")
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

def get_topics_score_by_brand(brand_competitor, competitors_df, sentiment_selected):
    df2 = competitors_df[competitors_df["brand"] == brand_competitor].copy()
    df2 = sentiment_aspect_df(df2)
    df2["count"] = df2["count"].astype(int)

    # sentiment_selected is 'positive' or 'negative'
    # but df2 contains 'pos' or 'neg' so sentiment_selected[:3]
    return df2[df2["sentiment"] == sentiment_selected[:3]]["count"].to_list()

def topic_comparison(competitors_df, competitor, color, topics, sentiment_selected):
    topics = topics[:10]  # momentaneo!!!
    topics.append(topics[0])

    values = get_topics_score_by_brand(competitor, competitors_df, sentiment_selected)[:10] # momentaneo!!!
    values.append(values[0])

    fig = go.Figure(
        data=go.Scatterpolar(
        r=values,
        theta=topics,
        fill="toself",
        fillcolor=color,
        line_color=color,
        mode=None,
        name=competitor,
    ))

    fig.update_layout(default_layout)
    fig.update_layout(
        polar = dict(radialaxis_range = [0, 100]),
        margin=dict(l=40, r=40, t=40, b=40),
        title={"text": competitor}
    )

    return fig


