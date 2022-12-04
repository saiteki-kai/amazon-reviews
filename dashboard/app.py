import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash

from reviews.config import asum_output_dir

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

data_df = pd.read_json(asum_output_dir / "reviews_sentiments.json.gz")
