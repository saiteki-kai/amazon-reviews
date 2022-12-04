def update_brand(data_df, brand, category):
    df = data_df[data_df["brand"] == brand].copy()

    if category and category != "All":
        df = df[df["category"] == category].copy()

    return df
