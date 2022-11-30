import numpy as np

from reviews.preprocess import remove_spaces

common = {
    "by",
    "limited",
    "llc",
    "ltd",
    "inc",
    "co",
    "corp",
    "corporated",
    "corporation",
}


def clean_brand(x):
    if type(x) is not str:
        return np.nan

    x = x.lower()
    x = (
        x.replace("\n", "")
        .replace(".", "")
        .replace(",", "")
        .replace("{", "")
        .replace("}", "")
    )
    x = x.strip()
    x = remove_spaces(x)
    x = x.strip()

    x = " ".join([t for t in x.split(" ") if t not in common])

    if len(x) <= 1 or "Top Ten" in x or len(x.split(" ")) > 7:
        return np.nan

    return x


def flat_sentence_tokens(tokens):
    return [token for row in tokens for sent in row for token in sent]
