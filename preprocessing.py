import re
import spacy
from nltk.stem import PorterStemmer
from spacy.lang.en.stop_words import STOP_WORDS


# --------------------------------------------------
# LOAD NLP TOOLS
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")

stemmer = PorterStemmer()


# --------------------------------------------------
# SCRIPT VALIDATION
# --------------------------------------------------

def validate_english_script(text):

    english_characters = re.findall(
        r"[A-Za-z]",
        text
    )

    total_letters = re.findall(
        r"[A-Za-z\u0900-\u097F]",
        text
    )

    if not total_letters:
        return {
            "valid": False,
            "message": "No alphabetic text detected."
        }

    english_ratio = (
        len(english_characters)
        / len(total_letters)
    )

    if english_ratio >= 0.80:

        return {
            "valid": True,
            "message": "Text is predominantly English."
        }

    return {
        "valid": False,
        "message": "Text contains significant non-English script."
    }


# --------------------------------------------------
# TOKENIZATION
# --------------------------------------------------

def tokenize_text(text):

    doc = nlp(text)

    tokens = []

    for token in doc:

        if not token.is_space:

            tokens.append(token.text)

    return tokens


# --------------------------------------------------
# TOKEN FILTRATION
# --------------------------------------------------

def filter_tokens(tokens):

    filtered_tokens = []

    for token in tokens:

        # Remove punctuation
        if re.fullmatch(r"[^\w]+", token):
            continue

        # Remove empty values
        if not token.strip():
            continue

        filtered_tokens.append(token)

    return filtered_tokens


# --------------------------------------------------
# STOP-WORD REMOVAL
# --------------------------------------------------

def remove_stopwords(tokens):

    result = []

    for token in tokens:

        if token.lower() not in STOP_WORDS:

            result.append(token)

    return result


# --------------------------------------------------
# STEMMING
# --------------------------------------------------

def stem_tokens(tokens):

    results = []

    for token in tokens:

        results.append({
            "word": token,
            "stem": stemmer.stem(token.lower())
        })

    return results


# --------------------------------------------------
# LEMMATIZATION
# --------------------------------------------------

def lemmatize_tokens(text):

    doc = nlp(text)

    results = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        results.append({
            "word": token.text,
            "lemma": token.lemma_
        })

    return results


# --------------------------------------------------
# WORD GENERATION
# --------------------------------------------------

def generate_words(tokens):

    generated_words = []

    for token in tokens:

        word = token.lower()

        if len(word) >= 3:

            generated_words.append(word)

    # Remove duplicates while preserving order
    generated_words = list(
        dict.fromkeys(generated_words)
    )

    return generated_words


# --------------------------------------------------
# COMPLETE PREPROCESSING
# --------------------------------------------------

def preprocess_text(text):

    script = validate_english_script(text)

    tokens = tokenize_text(text)

    filtered_tokens = filter_tokens(tokens)

    stopword_removed = remove_stopwords(
        filtered_tokens
    )

    stems = stem_tokens(
        stopword_removed
    )

    lemmas = lemmatize_tokens(text)

    generated_words = generate_words(
        stopword_removed
    )

    return {

        "script_validation": script,

        "tokens": tokens,

        "filtered_tokens": filtered_tokens,

        "stopword_removed": stopword_removed,

        "stems": stems,

        "lemmatization": lemmas,

        "generated_words": generated_words
    }