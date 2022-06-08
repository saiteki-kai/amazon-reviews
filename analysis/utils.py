import re
import unicodedata
from string import punctuation

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

STOPWORDS = set(stopwords.words("english"))
STOPWORDS.remove("not")
STOPWORDS.remove("nor")
STOPWORDS.remove("against")

PUNCTUATIONS = set(punctuation + "…")

URL_RE = r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"


def remove_urls(text):
    return re.sub(URL_RE, "", text)


def remove_spaces(text):
    return re.sub(" +", " ", text)


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_non_ascii(text):
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )


def normalize(words, lowercase=False):
    tokens = []
    for word in words:
        word = remove_non_ascii(word)
        if lowercase:
            word = word.lower()
        if word.lower() not in PUNCTUATIONS and word.lower() not in STOPWORDS:
            tokens.append(word)
    return tokens


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatize(words):
    wnl = WordNetLemmatizer()
    lemmas = []
    for word, pos in pos_tag(words):
        lemmas.append(wnl.lemmatize(word, get_wordnet_pos(pos)))
    return lemmas


def preprocess(text):
    text = strip_html(text)
    text = remove_urls(text)
    text = remove_spaces(text)
    text = contractions.fix(text)
    tokens = word_tokenize(text)
    tokens = normalize(tokens, lowercase=True)
    lemmas = lemmatize(tokens)
    return " ".join(lemmas)
