import pandas as pd
import gzip
import json

# get asin codes
prod_df =  pd.read_json("./data/meta_computers.json.gz")
asin = set(prod_df["asin"])
print("Products Metadata Loaded")

# try with more RAM
# df = pd.read_json("./data/Electronics_5.json.gz", orient="records")

i = 0
k = 0
data = []
with gzip.open("./data/Electronics_5.json.gz") as f:
  for l in f:
    review = json.loads(l.strip())
    
    if review.get("asin") in asin:
      # remove unwanted fields
      for field in ["reviewTime", "verified", "style", "reviewerID", "reviewerName", "image"]:
        review.pop(field, None)

      # append the review
      if review.get("reviewText") and review.get("summary"):
        data.append(review)
        i = i + 1

    # limit number of data
    if i > 100000:
      break

    if k % 50000 == 0:
      print(f"{i} / {k}")
    k = k + 1

print("finished")

df = pd.DataFrame(data)

# rename columns
df.rename(columns={"unixReviewTime": "timestamp", "reviewText": "text"}, inplace=True)

# delete duplicates
df.drop_duplicates(inplace=True)

# optimize memory
vote_cat = pd.CategoricalDtype(categories=[1, 2, 3, 4, 5])
df["overall"] = df["overall"].astype("uint8").astype(vote_cat)
df["vote"] = df["vote"].str.replace(",", "").fillna(0).astype("uint16")
df["asin"] = df["asin"].astype("category")
df["summary"] = df["summary"].astype("string")
df["text"] = df["text"].astype("string")
df["timestamp"] = pd.to_datetime(df["timestamp"])

df.info(verbose=True, memory_usage="deep")

df.to_json("./data/reviews_computers.json.gz", orient="records", compression="gzip")