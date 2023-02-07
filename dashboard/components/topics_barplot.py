from collections import Counter

import pandas as pd
import plotly.express as px

from dashboard.utils import default_layout, secondary_color


def topics_barplot(brand_df, perc=True):
    count = Counter()
    for x in brand_df["topics"].values:
        topics = set([y["name"] for y in x])
        count.update(topics)

    topics_count = pd.DataFrame(count.items(), columns=["topic", "count"])
    topics_count["topic"] = topics_count["topic"].astype("category")

    order = topics_count.sort_values(by="count", ascending=False)
    order = order.reset_index()["topic"]

    topics_count["percentage"] = topics_count["count"] / topics_count["count"].sum() * 100

    fig = px.bar(
        topics_count,
        y="topic",
        x="percentage" if perc else "count",
        color_discrete_sequence=[secondary_color],
        category_orders=dict(topic=order),
        title="Topics",
    )

    fig.update_layout(default_layout)

    if perc:
        fig.update_xaxes(ticksuffix="%")

    return fig, order
