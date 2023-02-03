import pandas as pd
import plotly.express as px

from dashboard.utils import default_layout, secondary_color


def category_barplot(brand_df, order):
    category_count = brand_df["category"].value_counts().reset_index()
    category_count_df = (
        pd.DataFrame(category_count).rename(columns={"category": "count", "index": "category"}).reset_index()
    )
    category_count_df["percentage"] = category_count_df["count"] / category_count_df["count"].sum() * 100

    fig = px.bar(
        category_count_df,
        x="percentage",
        y="category",
        color_discrete_sequence=[secondary_color],
        category_orders=order,
        title="Categories",
    )
    fig.update_layout(default_layout)
    fig.update_xaxes(ticksuffix="%")

    return fig
