import base64
import io
from collections import Counter

from wordcloud import WordCloud


def wordcloud(brand_df):
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

    # change the value to black
    def black_color_func(
        word, font_size, position, orientation, random_state=None, **kwargs
    ):
        return "hsl(0,100%, 1%)"

    img = io.BytesIO()
    wc = WordCloud(
        height=200,
        width=300,
        background_color="white",
        color_func=black_color_func,
        max_words=500,
    )
    wc.generate_from_frequencies(Counter(x))
    wc.recolor(color_func=black_color_func)
    wc.to_file("../output/wc.png")

    img_base64 = base64.b64encode(img.getvalue()).decode()

    return "data:image/png;base64,{}".format(img_base64)
