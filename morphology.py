import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


def analyze_morphology(text):

    doc = nlp(text)

    results = []

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        results.append({
            "word": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "morphology": str(token.morph)
        })

    return results