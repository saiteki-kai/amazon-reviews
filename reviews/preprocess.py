import importlib.resources
import re
import unicodedata

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
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
STOPWORDS.add("camera")

# Regular expressions

URL_RE = re.compile(
    r"(https?://(?:www\.|(?!www))[a-zA-Z\d][a-zA-Z\d-]+[a-zA-Z\d]\.\S{2,}|www\.[a-zA-Z\d][a-zA-Z\d-]+[a-zA-Z\d]\.\S{2,}|https?://(?:www\.|(?!www))[a-zA-Z\d]+\.\S{2,}|www\.[a-zA-Z\d]+\.\S{2,})"  # noqa: E501
)

SPACES_RE = re.compile(" +")

ALPHA_RE = re.compile(r"[^a-zA-Z\s]")

DOTS_RE = re.compile(r"\.{2,}")

NUM_RE = re.compile(r"(\d*\.?\d+(\w+)?)", flags=re.MULTILINE)

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

# init spell checker
speller = SymSpell()

RESOURCE_NAME = "frequency_dictionary_en_82_765.txt"
with importlib.resources.path("symspellpy", RESOURCE_NAME) as dictionary_path:
    speller.load_dictionary(dictionary_path, term_index=0, count_index=1)

# init lemmatizer
wnl = WordNetLemmatizer()

# init Stemmer
ps = PorterStemmer()


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


def remove_numbers(text):
    return NUM_RE.sub("", text)


def fix_punctuation(text):
    text = text.replace(",", ", ")  # split commas
    return DOT_SENT_RE.sub(r"\g<1>. \g<2>", text)  # split dots


def remove_special_chars(text):
    text = text.replace("-", " ")  # split dashes
    text = re.sub(r"/+|\\+", " ", text)  # split slashes
    text = text.replace("+", " ")  # split pluses

    return DOTS_RE.sub(" ", text)  # add a space after multiple dots


def remove_repetitions(text):
    return REP_CHAR_RE.sub(r"\1\1", text)


def normalize(words, lowercase=False, correct_spelling=True):
    tokens = []
    for word in words:
        # remove punctuation
        word = ALPHA_RE.sub("", word)

        # append words other than stopwords
        if len(word) != 0 and word.lower() not in STOPWORDS:
            token = remove_repetitions(word)

            if len(word) > 3 and correct_spelling:
                suggestions = speller.lookup(
                    word,
                    Verbosity.TOP,
                    transfer_casing=True,
                )
                if len(suggestions) > 0:
                    token = suggestions[0].term

            if lowercase:
                token = token.lower()

            tokens.append(token)

    return tokens


def get_wordnet_pos(treebank_tag):
    start = treebank_tag[0]
    return WORDNET_TAGS.get(start, wordnet.NOUN)


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


def stemming_sentences(sentences):
    sent_stems = []
    for sent in sentences:
        stems = []
        for word in sent:
            stems.append(ps.stem(word))
        sent_stems.append(stems)
    return sent_stems


def stemming(words):
    stems = []
    for word in words:
        stems.append(ps.stem(word))
    return stems


def preprocess(
    text,
    lowercase=True,
    sentences=True,
    return_tokens=True,
    lemmatization=True,
    correct_spelling=True,
):
    # text cleaning
    text = remove_urls(text)
    text = strip_html(text)
    text = remove_spaces(text)
    text = remove_non_ascii(text)
    text = remove_numbers(text)
    text = fix_punctuation(text)

    # expand contractions
    text = contractions.fix(text)

    if sentences:
        sent_tokens = []
        for sent in sent_tokenize(text):
            sent = remove_special_chars(sent)
            tokens = word_tokenize(sent)
            tokens = normalize(
                tokens,
                lowercase=lowercase,
                correct_spelling=correct_spelling,
            )

            if len(tokens) > 0:
                sent_tokens.append(tokens)

        if lemmatization:
            sent_tokens = lemmatize_sentences(sent_tokens)
        else:
            sent_tokens = stemming_sentences(sent_tokens)

        if return_tokens:
            return sent_tokens

        return [" ".join(sent) for sent in sent_tokens]

    text = remove_special_chars(text)
    tokens = word_tokenize(text)
    tokens = normalize(
        tokens,
        lowercase=lowercase,
        correct_spelling=correct_spelling,
    )

    if lemmatization:
        tokens = lemmatize(tokens)
    else:
        tokens = stemming(tokens)

    if return_tokens:
        return tokens

    return " ".join(tokens)
