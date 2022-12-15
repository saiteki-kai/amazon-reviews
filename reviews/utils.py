import json
import warnings
from collections import Counter
from itertools import chain
from pathlib import Path

import numpy as np

from reviews.config import data_dir
from reviews.preprocess import preprocess, remove_spaces

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

COMMON_BRAND_TERMS = {
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

    x = " ".join([t for t in x.split(" ") if t not in COMMON_BRAND_TERMS])

    if len(x) <= 1 or "Top Ten" in x or len(x.split(" ")) > 7:
        return np.nan

    return x


def read_sentiment_words(normalization=None):
    """
    Return positive and negative sentiment words
    based on the normalization.
    """
    with open(data_dir / "sentiwords.json", "r") as f:
        senti_words = json.load(f)

        if normalization not in {"stemming", "lemmatization"}:
            normalization = "raw"

        normalized = senti_words[normalization]

        pos_words = normalized["positive"]
        neg_words = normalized["negative"]

        return pos_words, neg_words


def flat_sentence_tokens(tokens):
    return [token for row in tokens for sent in row for token in sent]


def find_tokens_df(tokens_list):
    """
    Find tokens with a document frequency greater
    than 90% or less than 4.
    """

    word_freq = [Counter(chain.from_iterable(d)) for d in list(tokens_list)]

    doc_freq = Counter()
    for wf in word_freq:
        doc_freq.update(list(wf.keys()))

    common = [w for w, freq in doc_freq.items() if freq / len(doc_freq) > 0.9]

    rare = [w for w, freq in doc_freq.items() if freq < 4]

    return set(common), set(rare), set(common + rare)


def remove_tokens_df(df, tokens: set, field="tokens", inplace=False):
    """Remove a custom list of tokens from a dataframe."""

    res = (
        df[field]
        .apply(
            lambda review: [
                [t for t in sent if t not in tokens] for sent in review
            ]  # keep words not in 'tokens'
        )
        .apply(  # remove empty sentences
            lambda review: [sent for sent in review if sent]
        )
    )

    if inplace:
        df[field] = res
    else:
        return res


def preprocess_df(
    df,
    field="text",
    parallel=True,
    normalize=None,
    save=True,
    out_dir="",
    verbose=True,
    inplace=False,
):
    args = {}

    if normalize is not None:
        args[normalize] = True

    if not inplace:
        df = df.copy()

    if parallel:
        tokens = df[field].parallel_apply(lambda x: preprocess(x, **args))
    else:
        tokens = df[field].apply(lambda x: preprocess(x, **args))

    t1, t2, tokens_to_remove = find_tokens_df(tokens)

    if verbose:
        print(f"Common: {len(t1)}, Rare: {len(t2)}")
        print(f"Common: {t1}")

    df["tokens"] = tokens

    remove_tokens_df(df, tokens_to_remove, inplace=True)

    if verbose:

        def find_na(x):
            if len("".join(chain.from_iterable(x))) > 0:
                return x

            return None

        empty_docs = df["tokens"].apply(find_na).isna()
        print(f"Empty Docs: {empty_docs.sum() / len(df) * 100:.2f}%")

    if save and normalize is not None:
        df.to_json(Path(out_dir) / f"reviews_{field}_{normalize}.json.gz")

    return df
