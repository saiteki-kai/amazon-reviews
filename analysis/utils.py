import re
import subprocess
import unicodedata
from autocorrect import Speller
from string import punctuation

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

STOPWORDS = set(stopwords.words("english"))
STOPWORDS.remove("not")
STOPWORDS.remove("nor")
STOPWORDS.remove("against")

PUNCTUATIONS = set(punctuation)

URL_RE = r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"


spell = Speller()


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


def remove_special_chars(text):
    text = text.replace("/", " ")  # split slashes
    return re.sub(r"[^a-zA-z\s]", "", text)


def normalize(words, lowercase=False):
    tokens = []
    for word in words:
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


def preprocess(text, lowercase=True, sentences=True, return_tokens=True):
    # text cleaning
    text = strip_html(text)
    text = remove_urls(text)
    text = remove_spaces(text)
    text = remove_non_ascii(text)

    # correct spelling
    text = spell(text)

    # expand contractions
    text = contractions.fix(text)

    if sentences:
        sent_tokens = []
        for sent in sent_tokenize(text):
            sent = remove_special_chars(sent)
            tokens = word_tokenize(sent)
            tokens = normalize(tokens, lowercase=lowercase)
            lemmas = lemmatize(tokens)

            if len(lemmas) > 0:
                sent_tokens.append(lemmas)
        if return_tokens:
            return sent_tokens
        else:
            return [" ".join(sent) for sent in sent_tokens]
    else:
        text = remove_special_chars(text)
        tokens = word_tokenize(text)
        tokens = normalize(tokens, lowercase=lowercase)
        lemmas = lemmatize(tokens)

    if return_tokens:
        return lemmas
    else:
        return " ".join(lemmas)


def asum(inputDir, outputDir, alpha, beta, gamma, nTopics, iterations="1000"):
    subprocess.call(
        [
            "java",
            "-jar",
            "../bin/ASUM.jar",
            "-a",
            alpha,
            "-b",
            beta,
            "-g",
            gamma,
            "-t",
            nTopics,
            "-th",
            "3",
            "-i",
            iterations,
            "-d",
            inputDir,
            "-o",
            outputDir,
        ]
    )
