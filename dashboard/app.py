import dash_bootstrap_components as dbc
from dash import Dash

from dashboard.config import data_dir
from dashboard.utils import load_dataset

external_stylesheets = [
    dbc.themes.LUX,
    dbc.icons.FONT_AWESOME,
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

data_df = load_dataset(data_dir / "reviews.json.gz")
