def update_brand(data_df, brand, category, year):
    df = data_df[(data_df["brand"] == brand) & (data_df["timestamp"].dt.year == int(year))].copy()

    if category and category != "All":
        df = df[df["category"] == category].copy()

    return df


primary_color = "#ECE81A"
secondary_color = "#C3C5C5"

default_layout = {
    "margin": dict(l=0, t=30, r=0, b=0),
    "title_pad": dict(t=0, b=0),
    "legend_orientation": "h",
    # "legend_yanchor": "bottom",
    # "legend_y": 1.02,
    # "legend_x": 1,
    # "legend_xanchor": "right",
    # "legend_title": "",
    # "hovermode": False,
    "dragmode": False,
    "plot_bgcolor": "#fff",
    "modebar_orientation": "v",
    "xaxis": dict(showgrid=False, title_text=""),
    "yaxis": dict(showgrid=False, title_text=""),
}
