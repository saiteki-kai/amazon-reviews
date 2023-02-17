import os
from pathlib import Path

root_dir = Path(os.path.dirname(os.path.realpath(__file__)))
data_dir = root_dir / "data"

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
