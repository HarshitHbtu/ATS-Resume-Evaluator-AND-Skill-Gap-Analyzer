import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):

    text = text.lower()

    text = text.translate(str.maketrans("", "", string.punctuation))

    text = re.sub(r"\d+", "", text)

    text = re.sub(r"\s+", " ", text)

    words = text.split()

    words = [word for word in words if word not in stop_words]

    words = [lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)


def extract_degree(text):

    text = text.lower()

    if "phd" in text:
        return "phd"

    elif "master" in text:
        return "masters"

    elif "bachelor" in text or "b.tech" in text or "btech" in text:
        return "bachelors"

    elif "diploma" in text:
        return "diploma"

    else:
        return "high school"


def has_portfolio(text):

    text = text.lower()

    keywords = [
        "github",
        "portfolio",
        "linkedin",
        "leetcode",
        "codechef",
        "codeforces",
        "codolio"
    ]

    for keyword in keywords:
        if keyword in text:
            return True

    return False
