import pandas as pd
import plotly.express as px

from dashboard.utils import default_layout, secondary_color


def category_barplot(brand_df, order):
    category_count = brand_df["category"].value_counts().reset_index()
    category_count_df = (
        pd.DataFrame(category_count)
        .rename(columns={"category": "count", "index": "category"})
        .reset_index()
    )
    fig = px.bar(
        category_count_df,
        x="count",
        y="category",
        color_discrete_sequence=[secondary_color],
        category_orders=order,
        title="Categories",
    )
    fig.update_layout(default_layout)

    return fig
