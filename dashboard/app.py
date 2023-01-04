import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash

from reviews.config import asum_output_dir

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME,
    "./assets/style.css",
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

data_df = pd.read_json(asum_output_dir / "reviews_sentiments.json.gz")
data_df = data_df[
    data_df["brand"].isin(list(data_df["brand"].value_counts()[:100].index))
]

topic_set = {
    "power supply system",
    "case",
    "brand",
    "drivers",
    "pc replacement / upgrade",
    "network",
    "storage",
    "monitor",
    "aesthetic",
    "temperature",
    "audio/video cards",
    "cooling system",
    "price",
    "build",
    "installation",
    "sound card",
    "recommended",
    "processor",
    "thermal paste",
    "performance",
    "service",
    "gaming",
    "quality",
    "memory",
    "graphic card",
    "motherboard",
}
