import gzip
import json

import pandas as pd

from reviews.config import processed_data_dir, raw_data_dir

fields_to_remove = {
    "tech1",
    "tech2",
    "main_cat",
    "feature",
    "rank",
    "fit",
    "also_buy",
    "also_view",
    "similar_item",
    "imageURL",
    # "imageURLHighRes",
    "details",
    "date",
}

# load data
data = []
with gzip.open(raw_data_dir / "meta_Electronics.json.gz") as f:
    for line in f:
        prod = json.loads(line.strip())

        # filter category
        sub_categories = list(prod["category"])
        if (
            len(sub_categories) > 4
            and sub_categories[1] == "Computers & Accessories"
            and sub_categories[2] == "Computer Components"
            and sub_categories[3] == "Internal Components"
        ):
            # remove unwanted fields
            [prod.pop(field, None) for field in fields_to_remove]
            data.append(prod)

# create the data frame
df = pd.DataFrame(data)
print(len(df))

# remove rows with unformatted title (some 'title' may contain html content)
df = df.fillna("")
df = df[~df.title.str.contains("getTime")]
print(len(df))

# remove duplicates
df = df.drop_duplicates(subset=["asin"])
print(len(df))

# save the data frame
df.to_json(
    processed_data_dir / "meta.json.gz",
    orient="records",
    compression="gzip",
)
