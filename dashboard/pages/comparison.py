import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

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



# function for dynamic dash page
@callback([Output('dropdown_left', "placeholder"), Output('dropdown_right', "placeholder")], [Input('dropdown_down_comparison', 'value')])
def drop_down_kind_comparison(value):
    if(str(value) == "None"):
        return "Select your kind of comparison", "Select your kind of comparison"
    else:
        return "Select your " + str(value), "Select your " + str(value)