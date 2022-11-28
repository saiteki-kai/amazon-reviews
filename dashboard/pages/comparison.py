import dash_bootstrap_components as dbc
from dash import html

layout = html.Div(
    [
        dbc.Container(
            [
                html.H1("Comparison"),
            ],
            className="py-3",
        ),        
        dbc.Row([
            dbc.Col(html.Div("prima linea grafici,primo grafico")),
            dbc.Col(html.Div("prima linea grafici,secondo grafico")),
            dbc.Col(html.Div("prima linea grafici,terzo grafico")),
        ]),
        dbc.Row([
            dbc.Col(html.Div("seconda linea grafici, primo grafico")),
            dbc.Col(html.Div("seconda linea grafici, secondo grafico")),
        ]),
    ]
)

