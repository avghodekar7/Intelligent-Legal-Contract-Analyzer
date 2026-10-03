import spacy
from collections import Counter


# --------------------------------------------------
# LOAD ENGLISH NLP MODEL
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# POS TAGGING
# --------------------------------------------------

def analyze_pos(text):

    doc = nlp(text)

    results = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        results.append({
            "word": token.text,
            "pos": token.pos_,
            "tag": token.tag_,
            "description": spacy.explain(token.pos_)
        })

    return results


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

def analyze_chunks(text):

    doc = nlp(text)

    chunks = []

    for chunk in doc.noun_chunks:

        chunks.append({
            "text": chunk.text,
            "root": chunk.root.text,
            "root_pos": chunk.root.pos_
        })

    return chunks


# --------------------------------------------------
# N-GRAM GENERATION
# --------------------------------------------------

def generate_ngrams(text):

    doc = nlp(text)

    tokens = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        tokens.append(token.text.lower())

    # ----------------------------------------------
    # UNIGRAMS
    # ----------------------------------------------

    unigrams = tokens

    # ----------------------------------------------
    # BIGRAMS
    # ----------------------------------------------

    bigrams = []

    for i in range(len(tokens) - 1):

        bigrams.append(
            f"{tokens[i]} {tokens[i + 1]}"
        )

    # ----------------------------------------------
    # TRIGRAMS
    # ----------------------------------------------

    trigrams = []

    for i in range(len(tokens) - 2):

        trigrams.append(
            f"{tokens[i]} {tokens[i + 1]} "
            f"{tokens[i + 2]}"
        )

    # ----------------------------------------------
    # FREQUENCY
    # ----------------------------------------------

    unigram_frequency = Counter(unigrams)
    bigram_frequency = Counter(bigrams)
    trigram_frequency = Counter(trigrams)

    return {
        "unigrams": unigrams,
        "bigrams": bigrams,
        "trigrams": trigrams,
        "unigram_frequency": dict(
            unigram_frequency.most_common(20)
        ),
        "bigram_frequency": dict(
            bigram_frequency.most_common(20)
        ),
        "trigram_frequency": dict(
            trigram_frequency.most_common(20)
        )
    }


# --------------------------------------------------
# COMPLETE LINGUISTIC ANALYSIS
# --------------------------------------------------

def analyze_linguistics(text):

    return {
        "pos": analyze_pos(text),
        "chunks": analyze_chunks(text),
        "ngrams": generate_ngrams(text)
    }