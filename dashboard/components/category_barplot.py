import pandas as pd
import plotly.express as px


def category_barplot(brand_df, order):
    category_count = brand_df["category"].value_counts().reset_index()
    category_count_df = (
        pd.DataFrame(category_count)
        .rename(columns={"category": "count", "index": "category"})
        .reset_index()
    )
    fig1 = px.bar(
        category_count_df,
        x="count",
        y="category",
        color_discrete_sequence=["#108de4"],
        category_orders=order,
    )
    fig1.update_xaxes(showgrid=False, title_text="")
    fig1.update_yaxes(showgrid=False, title_text="")
    fig1.update_layout(margin=dict(l=0, t=0, r=0, b=0))

    return fig1
