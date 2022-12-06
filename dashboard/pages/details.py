import datetime
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html
from reviews.config import processed_data_dir
import pandas as pd
import plotly.express as px

layout = html.Div(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    dbc.ListGroup(id = "group_list"),
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([]),
                        dbc.Col([]),
                        dbc.Col([]),
                    ]),
                    dbc.Row([]),
                ]),
            ]),
        ],
        className="py-3",
    ),
)

# function for dynamic dash page -----------------------------------------------
from dashboard.app import data_df
from dashboard.utils import update_brand
import dash

@dash.callback(
    Output("group_list", "children"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)

def update_plot(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    #dbc.ListGroup(