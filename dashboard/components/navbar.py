import dash_bootstrap_components as dbc

layout = dbc.Navbar(
    dbc.Container(
        dbc.Nav(
            children=[
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Products", href="/details", active="exact"),
                dbc.NavLink("Comparison", href="/comparison", active="exact"),
            ],
        ),
        fluid=True,
    ),
)
