from collections import Counter

from wordcloud import WordCloud


def wordcloud(brand_df):
    wc_sentiment = None
    wc_df = brand_df
    if wc_sentiment == "positive" or wc_sentiment == "negative":
        wc_df = brand_df[brand_df["sentiment"] == wc_sentiment]
    x = ["".join(token) for review in wc_df["tokens"] for sentence in review for token in sentence]

    # change the value to black
    def black_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0,100%, 1%)"

    wc = WordCloud(
        height=500,
        width=750,
        background_color="white",
        color_func=black_color_func,
        max_words=200,
    )
    wc.generate_from_frequencies(Counter(x))
    wc.recolor(color_func=black_color_func)
    return wc.to_image()
