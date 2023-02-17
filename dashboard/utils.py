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


def update_options(from_year, to_year):
    options = [
        {"label": "Day", "value": "D"},
        {"label": "Week", "value": "W"},
        {"label": "Month", "value": "M"},
    ]

    if from_year != to_year:
        options.extend([{"label": "Year", "value": "Y"}])

    return options, options[-1]["value"]


def load_dataset(path):
    data_df = pd.read_json(path)
    data_df = data_df[data_df["brand"].isin(list(data_df["brand"].value_counts()[:40].index))].copy()

    categories = data_df.groupby(["brand"])["category"].value_counts().rename("count").reset_index()
    brand_cats = categories[categories["count"] > 30][["brand", "category"]]

    data_df = data_df.merge(brand_cats, on=["brand", "category"])

    data_df["brand"] = data_df["brand"].astype("string").astype("category").astype("string")
    data_df["category"] = data_df["category"].astype("string").astype("category").astype("string")

    topic_set = {
        "Satisfaction",
        "Price",
        "Quality",
        "Performance",
        "Delivery",
        "Motherboard",
        "Processor",
        "Power Supply",
        "Memory",
        "Cooling System",
        "Installation",
        "Aesthetic",
        "Sound",
        "Video",
        "Temperature",
        "Thermal Paste",
        "Overclocking",
    }

    data_df["topics"] = data_df["topics"].apply(lambda x: [y for y in x if y["name"] in topic_set])

    return data_df
