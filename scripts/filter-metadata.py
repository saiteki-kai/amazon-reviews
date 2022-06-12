import pandas as pd
import gzip
import json

import sys;
sys.path.append('.')

from reviews.config import raw_data_dir, processed_data_dir

fields_to_remove = set(
    [
        "tech1",
        "tech2",
        # "brand",
        "feature",
        "rank",
        "fit",
        "also_buy",
        "also_view",
        "similar_item",
        # "price",
        "imageURL",
        "imageURLHighRes",
        "details",
    ]
)

# load data
data = []
with gzip.open(raw_data_dir / "meta_Electronics.json.gz") as f:
    for l in f:
        prod = json.loads(l.strip())

        # filter category
        sub_categories = list(prod["category"])
        if (
            len(sub_categories) > 2
            and sub_categories[1] == "Camera & Photo"
            and sub_categories[2] == "Digital Cameras"
        ):
            # remove unwanted fields
            [prod.pop(field, None) for field in fields_to_remove]
            data.append(prod)

# create the data frame
df = pd.DataFrame.from_dict(data)
print(len(df))

# remove rows with unformatted title (i.e. some 'title' may still contain html style content)
df = df.fillna("")
df = df[~df.title.str.contains("getTime")]
print(len(df))

# remove duplicates
df = df.drop_duplicates(subset=["asin"])
print(len(df))

# save the data frame
df.to_json(
    processed_data_dir / "meta_digital_cameras.json.gz",
    orient="records",
    compression="gzip",
)
