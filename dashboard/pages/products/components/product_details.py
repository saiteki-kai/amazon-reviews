import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

from dashboard.app import data_df


def stars_icon(rating):
    filled_star = html.I(className="fa-solid fa-star")
    half_star = html.I(className="fa-solid  fa-star-half-stroke")
    empty_star = html.I(className="fa-regular fa-star")

    half = [half_star] if int(rating) != rating else []
    rating = int(rating)

    return html.Div(([filled_star] * rating) + half + ([empty_star] * (5 - rating - len(half))))


def get_details(asin):
    prods_df = data_df.drop_duplicates(["asin"])
    prods_df = prods_df.set_index("asin")[["title", "description", "category", "imageURLHighRes"]]

    mean_values = data_df.groupby("asin")["overall"].mean()
    prods_df = pd.merge(prods_df, mean_values, on="asin")

    prod_exists = asin in set(prods_df.index)

    if prod_exists:
        prod = prods_df.loc[asin]

        return [
            html.H5(prod["title"], id="prod-title"),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.Img(src=prod["imageURLHighRes"], alt="No Image Available"),
                            id="prod-img",
                        ),
                        className="h-100",
                    ),
                    dbc.Col(
                        [
                            stars_icon(prod["overall"]),
                            html.P(prod["description"], id="prod-desc"),
                        ],
                        className="h-100",
                        id="description",
                    ),
                ],
                className="g-0 scroll",
            ),
        ]

    return []
