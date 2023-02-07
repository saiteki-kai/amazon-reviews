import pandas as pd


def update_brand(data_df, brand, category, from_year, to_year):
    if int(from_year) >= int(to_year):
        to = int(from_year)
    else:
        to = int(to_year)

    to = pd.Timestamp(year=to, month=12, day=31)

    year_mask = (data_df["timestamp"] >= from_year) & (data_df["timestamp"] <= to)
    df = data_df[(data_df["brand"] == brand) & year_mask].copy()

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
