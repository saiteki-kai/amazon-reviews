import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html
from reviews.config import processed_data_dir
import pandas as pd

layout = html.Div(
    [
        dbc.Container(
            [
                html.H1("Comparison"),
            ],
            className="py-3",
        ),   
        dbc.Row([   
            dbc.Row([
                dbc.Row(
                    dbc.Col(html.Div(
                        dcc.Dropdown(['Brand', 'Product', 'Sub-category'], placeholder='Select kind of comparison . . . ', id='dropdown_down_comparison')
                    )),
                ),
                dbc.Row([
                    dbc.Col(html.Div(
                        dcc.Dropdown(['NYC', 'MTL', 'SF'], placeholder='Select your kind', id='dropdown_left')
                    )),
                    dbc.Col(html.Div(
                        dcc.Dropdown(['NYC', 'MTL', 'SF'], placeholder='Select your kind', id='dropdown_right')
                    )),
                ]),
            ]),
            dbc.Row([ 
                dbc.Row([
                    dbc.Col(html.Div("prima linea grafici,primo grafico")),
                    dbc.Col(html.Div("prima linea grafici,secondo grafico")),
                    dbc.Col(html.Div("prima linea grafici,terzo grafico")),
                ]),
                dbc.Row([
                    dbc.Col(html.Div("seconda linea grafici, primo grafico")),
                    dbc.Col(html.Div("seconda linea grafici, secondo grafico")),
                ]),
            ]),
        ])
    ]
)

# function for dynamic dash page -----------------------------------------------
#variable
data_df = pd.read_json(processed_data_dir / "products_reviews.json.gz")

# dynamic set placeholder for dropdown left and right
@callback([Output('dropdown_left', "placeholder"), Output('dropdown_right', "placeholder")], [Input('dropdown_down_comparison', 'value')])
def drop_down_placeholder_kind_comparison(value):
    if(str(value) == "None"):
        return "Select your kind of comparison", "Select your kind of comparison"
    else:
        return "Select your " + str(value), "Select your " + str(value),

# dynamic set value for dropdown left and right 
@callback([Output('dropdown_left', "options"), Output('dropdown_right', "options")],[Input('dropdown_down_comparison', 'value')])
def drop_down_value(value):
    if(str(value) == "None"):
        return [],[]
    else:
        return data_df["brand"].to_dict() , ["valori"]