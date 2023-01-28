import plotly.express as px


def sentiment_piechart(data_df):
    return px.pie(
        data_df["sentiment"].value_counts(),
        values="sentiment",
        color_discrete_sequence=["#f54242", "#27d957"],
        names=["positive", "negative"],
        hole=0.65,
    )
