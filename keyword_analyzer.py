import spacy
from collections import Counter


# --------------------------------------------------
# LOAD ENGLISH NLP MODEL
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# KEYWORD EXTRACTION
# --------------------------------------------------

def extract_keywords(text, limit=20):

    doc = nlp(text)

    keywords = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        if token.is_stop:
            continue

        if token.like_num:
            continue

        if not token.is_alpha:
            continue

        word = token.lemma_.lower().strip()

        if len(word) < 3:
            continue

        keywords.append(word)

    frequency = Counter(keywords)

    top_keywords = frequency.most_common(limit)

    return [
        {
            "word": word,
            "frequency": count
        }
        for word, count in top_keywords
    ]


# --------------------------------------------------
# LEGAL KEYWORD EXTRACTION
# --------------------------------------------------

def extract_legal_keywords(text):

    doc = nlp(text)

    legal_keywords = []

    legal_terms = {
        "agreement",
        "contract",
        "payment",
        "salary",
        "confidentiality",
        "confidential",
        "termination",
        "terminate",
        "notice",
        "liability",
        "liable",
        "indemnity",
        "indemnification",
        "obligation",
        "employee",
        "employer",
        "party",
        "parties",
        "compensation",
        "invoice",
        "damages",
        "disclosure",
        "proprietary"
    }

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        lemma = token.lemma_.lower()

        if lemma in legal_terms:

            legal_keywords.append(lemma)

    frequency = Counter(legal_keywords)

    return [
        {
            "word": word,
            "frequency": count
        }
        for word, count in frequency.most_common(20)
    ]


# --------------------------------------------------
# CHART DATA
# --------------------------------------------------

def create_keyword_chart_data(keywords):

    labels = []
    frequencies = []

    for item in keywords:

        labels.append(item["word"])
        frequencies.append(item["frequency"])

    return {
        "labels": labels,
        "frequencies": frequencies
    }


# --------------------------------------------------
# COMPLETE KEYWORD ANALYSIS
# --------------------------------------------------

def analyze_keywords(text):

    keywords = extract_keywords(text)

    legal_keywords = extract_legal_keywords(text)

    keyword_chart = create_keyword_chart_data(
        keywords
    )

    legal_keyword_chart = create_keyword_chart_data(
        legal_keywords
    )

    return {
        "keywords": keywords,
        "legal_keywords": legal_keywords,
        "keyword_chart": keyword_chart,
        "legal_keyword_chart": legal_keyword_chart
    }