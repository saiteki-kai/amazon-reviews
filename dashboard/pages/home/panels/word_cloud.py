import base64
import io
from collections import Counter

import dash
from dash import Input, Output, html
from wordcloud import WordCloud

from dashboard.app import data_df
from dashboard.utils import update_brand


@dash.callback(
    Output("wordcloud-img", "src"),
    Input("brand-select", "value"),
    Input("category-select", "value"),
)
def update_word_cloud(brand, category):
    # update graph brand
    brand_df = update_brand(data_df, brand, category)

    wc_sentiment = None
    wc_df = brand_df
    if wc_sentiment == "positive" or wc_sentiment == "negative":
        wc_df = brand_df[brand_df["sentiment"] == wc_sentiment]
    x = [
        "".join(token)
        for review in wc_df["tokens"]
        for sentence in review
        for token in sentence
    ]

    c = Counter(x)

    # mask = np.array(Image.open("~/Downloads/accessori-featured.jpg"))
    # mask = mask, contour_width = 3, contour_color = 'steelblue'

    img = io.BytesIO()
    w = WordCloud(
        width=2400, height=800, background_color="black", colormap="Blues"
    ).fit_words(c)
    w.to_image().save(img, format="PNG")

    img_base64 = base64.b64encode(img.getvalue()).decode()

    return "data:image/png;base64,{}".format(img_base64)


panel = (
    html.Div(
        html.Img(id="wordcloud-img"),
        className="panel",
    ),
)
