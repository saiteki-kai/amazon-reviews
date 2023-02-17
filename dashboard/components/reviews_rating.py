import pandas as pd
import plotly.express as px

from dashboard.config import default_layout, secondary_color


def reviews_rating(reviews_df):
    rating_df = (
        reviews_df["overall"]
        .value_counts(normalize=True)
        .reset_index()
        .rename(columns={"index": "rating", "overall": "percentage"})
    )

    rating_df = pd.DataFrame(rating_df)
    rating_df["rating"] = rating_df["rating"].astype("category")
    # rating_df["color"] = rating_df["rating"].apply(
    #    lambda x: primary_color if x == 5 else secondary_color
    # )
    rating_df["percentage"] = rating_df["percentage"] * 100
    order = [1, 2, 3, 4, 5]

    fig = px.bar(
        rating_df,
        y="rating",
        x="percentage",
        color_discrete_sequence=[secondary_color],
        category_orders={"rating": order},
        # color="color",
        title="Rating",
    )

    fig.update_xaxes(ticksuffix="%")
    fig.update_layout(default_layout)
    fig.update_layout(
        {
            "yaxis": {
                "tickvals": order,
                "ticktext": [" ".join((["★"] * r) + (["☆"] * (5 - r))) for r in order],
            },
            "showlegend": False,
        }
    )

    return fig
