import re
import unicodedata

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.sentiment.util import mark_negation
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

STOPWORDS = set(stopwords.words("english"))

# Regular expressions

URL_RE = re.compile(
    r"(https?://(?:www\.|(?!www))[a-zA-Z\d][a-zA-Z\d-]+[a-zA-Z\d]\.\S{2,}|www\.[a-zA-Z\d][a-zA-Z\d-]+[a-zA-Z\d]\.\S{2,}|https?://(?:www\.|(?!www))[a-zA-Z\d]+\.\S{2,}|www\.[a-zA-Z\d]+\.\S{2,})"  # noqa: E501
)

SPACES_RE = re.compile(" +")

ALPHA_RE = re.compile(r"[^a-zA-Z\s]")

SPLIT_RE = re.compile(r"/+|\\+|\+|-|\.{2,}")

NUM_RE = re.compile(r"(\d*[.,]?\d+(\w+)?)", flags=re.MULTILINE)

DOT_SENT_RE = re.compile(
    r"([^\d.,\s]{2,})\.((?!com|net|txt)[a-zA-Z]+)", flags=re.MULTILINE
)

REP_CHAR_RE = re.compile(r"([A-Za-z])\1+", re.DOTALL)

WORDNET_TAGS = {
    "N": wordnet.NOUN,
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "R": wordnet.ADV,
}

# init lemmatizer
wnl = WordNetLemmatizer()

# init stemmer
ss = SnowballStemmer("english")


def remove_urls(text: str):
    """Remove URLs."""
    return URL_RE.sub("", text)


def remove_spaces(text: str):
    """Remove unnecessary spaces by keeping one."""
    return SPACES_RE.sub(" ", text)


def strip_html(text: str):
    """Remove html tags and replace html entities."""
    soup = BeautifulSoup(text, "html.parser")

    return soup.get_text()


def remove_non_ascii(text: str):
    """Replace non-ASCII characters with ASCII ones."""
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )


def remove_numbers(text: str):
    """Remove the numbers with their units of measurement."""
    return NUM_RE.sub("", text)


def fix_punctuation(text: str):
    """Spaces commas and dots."""
    text = text.replace(",", ", ")  # split commas

    return DOT_SENT_RE.sub(r"\g<1>. \g<2>", text)  # split dots


def space_special_chars(text: str):
    """Replace dashes, slashes, pluses and multiple dots with a space."""
    return SPLIT_RE.sub(" ", text)


def remove_repetitions(text: str):
    """Remove repeating alphabetic characters."""
    return REP_CHAR_RE.sub(r"\1\1", text)


def get_wordnet_pos(treebank_tag):
    start = treebank_tag[0].upper()
    return WORDNET_TAGS.get(start, wordnet.NOUN)


def normalize(
    tokens,
    tags=None,
    lowercase=True,
    lemmatization=True,
    stemming=False,
):
    if lemmatization and stemming:
        raise ValueError(
            "Arguments lemmatization and stemming cannot both be true.",
        )

    negs = mark_negation(tokens, double_neg_flip=True)
    negs = [neg.endswith("_NEG") for neg in negs]

    normalized_tokens = []
    for i, token in enumerate(tokens):
        token = ALPHA_RE.sub("", token)
        token = remove_repetitions(token)

        if len(token) > 0 and token.lower() not in STOPWORDS:
            if lowercase:
                token = token.lower()

            if lemmatization:
                pos = tags[i]
                token = wnl.lemmatize(token, pos)

            if stemming:
                token = ss.stem(token)

            if negs[i]:
                token = token + "_NEG"

            normalized_tokens.append(token)

    return normalized_tokens


def preprocess(
    text,
    lowercase=True,
    sentences=True,
    stemming=False,
    lemmatization=False,
    return_tokens=True,
):
    # text cleaning
    text = remove_urls(text)
    text = strip_html(text)
    text = remove_spaces(text)
    text = remove_non_ascii(text)
    text = remove_numbers(text)
    text = fix_punctuation(text)
    text = space_special_chars(text)

    # expand contractions
    text = contractions.fix(text)

    if sentences:
        tokens = [
            s_tokens
            for sent in sent_tokenize(text)
            if len(s_tokens := word_tokenize(sent)) > 0
        ]

        if lemmatization:
            sent_tags = [
                [(w, get_wordnet_pos(tag)) for w, tag in tag_sent]
                for tag_sent in pos_tag_sents(tokens)
            ]

            sent_tokens = []
            for tagged_sent in sent_tags:
                tokens, tags = list(zip(*tagged_sent))
                tokens = list(tokens)
                tags = list(tags)

                normalized_tokens = normalize(
                    tokens,
                    tags=tags,
                    lowercase=lowercase,
                    lemmatization=lemmatization,
                    stemming=stemming,
                )

                if len(normalized_tokens) > 0:
                    sent_tokens.append(normalized_tokens)

        else:
            sent_tokens = []
            for sent_token in tokens:
                normalized_tokens = normalize(
                    sent_token,
                    lowercase=lowercase,
                    lemmatization=lemmatization,
                    stemming=stemming,
                )
                if len(normalized_tokens) > 0:
                    sent_tokens.append(normalized_tokens)

        if return_tokens:
            return sent_tokens

        return [" ".join(sent) for sent in sent_tokens]

    tokens = word_tokenize(text)

    tags = None
    if lemmatization:
        tags = [get_wordnet_pos(tag) for _, tag in pos_tag(tokens)]

    normalized_tokens = normalize(
        tokens,
        tags,
        lowercase=lowercase,
        lemmatization=lemmatization,
        stemming=stemming,
    )

    if return_tokens:
        return normalized_tokens

    return " ".join(normalized_tokens)
