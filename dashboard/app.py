import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash

from reviews.config import asum_output_dir

external_stylesheets = [
    dbc.themes.LUX,
    dbc.icons.FONT_AWESOME,
    # "./assets/style.css",
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

data_df = pd.read_json(asum_output_dir / "reviews_sentiments.json.gz")
data_df = data_df[data_df["brand"].isin(list(data_df["brand"].value_counts()[:40].index))]

categories = data_df.groupby(["brand"])["category"].value_counts().rename("count").reset_index()
brand_cats = categories[categories["count"] > 30][["brand", "category"]]

data_df = data_df.merge(brand_cats, on=["brand", "category"])

data_df["brand"] = data_df["brand"].astype("string").astype("category").astype("string")
data_df["category"] = data_df["category"].astype("string").astype("category").astype("string")

topic_set = {
    "Satisfaction",
    "Price",
    "Quality",
    "Performance",
    "Delivery",
    "Motherboard",
    "Processor",
    "Power Supply",
    "Memory",
    "Cooling System",
    "Installation",
    "Aesthetic",
    "Sound",
    "Video",
    "Temperature",
    "Thermal Paste",
    "Overclocking",
}

data_df["topics"] = data_df["topics"].apply(lambda x: [y for y in x if y["name"] in topic_set])
