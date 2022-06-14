import importlib.resources
import re
import unicodedata

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import sent_tokenize, word_tokenize
from symspellpy import SymSpell, Verbosity

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

STOPWORDS = set(stopwords.words("english"))
STOPWORDS.remove("not")
STOPWORDS.remove("nor")
STOPWORDS.remove("against")

# Regular expressions

URL_RE = re.compile(
    r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"  # noqa: E501
)

SPACES_RE = re.compile(" +")

ALPHA_RE = re.compile(r"[^a-zA-z\s]")


# init spell checker
speller = SymSpell()

resource_name = "frequency_dictionary_en_82_765.txt"
with importlib.resources.path("symspellpy", resource_name) as dictionary_path:
    speller.load_dictionary(dictionary_path, term_index=0, count_index=1)

# init lemmatizer
wnl = WordNetLemmatizer()

wordnet_tags = {
    "N": wordnet.NOUN,
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "R": wordnet.ADV,
}


def remove_urls(text):
    return URL_RE.sub("", text)


def remove_spaces(text):
    return SPACES_RE.sub(" ", text)


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
    return ALPHA_RE.sub("", text)


def normalize(words, lowercase=False):
    tokens = []
    for word in words:
        if lowercase:
            word = word.lower()
        if word.lower() not in STOPWORDS:
            suggestions = speller.lookup(word, Verbosity.CLOSEST)
            if len(suggestions) > 0:
                tokens.append(suggestions[0].term)
            else:
                tokens.append(word)
    return tokens


def get_wordnet_pos(treebank_tag):
    start = treebank_tag[0]
    return wordnet_tags.get(start, wordnet.NOUN)


def lemmatize_sentences(sentences):
    sent_lemmas = []
    for pos_sent in pos_tag_sents(sentences):
        lemmas = []
        for word, pos in pos_sent:
            lemmas.append(wnl.lemmatize(word, get_wordnet_pos(pos)))
        sent_lemmas.append(lemmas)
    return sent_lemmas


def lemmatize(words):
    lemmas = []
    for word, pos in pos_tag(words):
        lemmas.append(wnl.lemmatize(word, get_wordnet_pos(pos)))
    return lemmas


def preprocess(text, lowercase=True, sentences=True, return_tokens=True):
    # text cleaning
    text = remove_urls(text)
    text = strip_html(text)
    text = remove_spaces(text)
    text = remove_non_ascii(text)

    # expand contractions
    text = contractions.fix(text)

    if sentences:
        sent_tokens = []
        for sent in sent_tokenize(text):
            sent = remove_special_chars(sent)
            tokens = word_tokenize(sent)
            tokens = normalize(tokens, lowercase=lowercase)

            if len(tokens) > 0:
                sent_tokens.append(tokens)

        sent_lemmas = lemmatize_sentences(sent_tokens)

        if return_tokens:
            return sent_lemmas
        else:
            return [" ".join(sent) for sent in sent_lemmas]
    else:
        text = remove_special_chars(text)
        tokens = word_tokenize(text)
        tokens = normalize(tokens, lowercase=lowercase)
        lemmas = lemmatize(tokens)

    if return_tokens:
        return lemmas
    else:
        return " ".join(lemmas)
