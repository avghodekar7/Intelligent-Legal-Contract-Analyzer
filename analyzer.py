import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# LEGAL ENTITY EXTRACTION
# --------------------------------------------------

def extract_legal_entities(doc):

    entities = []

    # ----------------------------------------------
    # 1. PERSON / ORGANIZATION / DATE FROM SPACY
    # ----------------------------------------------

    for ent in doc.ents:

        # Ignore known incorrect generic predictions
        if ent.text.lower() == "monthly":
            continue

        if ent.text.lower() == "thirty days":
            continue

        if ent.label_ == "ORG" and ent.text.upper().startswith("INR"):
            continue

        # Improve organization name
        if ent.label_ == "ORG":
            text = ent.text

            # If "Ltd." immediately follows the entity,
            # include it in the organization name.
            following_tokens = []

            for token in doc[ent.end:ent.end + 2]:
                following_tokens.append(token.text)

            if "Ltd." in following_tokens:
                text = text + " Ltd."

            entities.append({
                "text": text,
                "label": "ORGANIZATION",
                "description": "Company, institution or organization"
            })

        elif ent.label_ == "PERSON":
            entities.append({
                "text": ent.text,
                "label": "PERSON",
                "description": "Person name"
            })

        elif ent.label_ == "DATE":
            entities.append({
                "text": ent.text,
                "label": "DATE",
                "description": "Contract date"
            })

    # ----------------------------------------------
    # 2. MONEY
    # ----------------------------------------------

    money_pattern = re.compile(
        r"\b(?:INR|Rs\.?)\s*[\d,]+(?:\.\d+)?"
    )

    for match in money_pattern.finditer(doc.text):

        entities.append({
            "text": match.group(),
            "label": "MONEY",
            "description": "Monetary value"
        })

    # ----------------------------------------------
    # 3. NOTICE PERIOD
    # ----------------------------------------------

    number_words = (
        "one|two|three|four|five|six|seven|eight|nine|ten|"
        "eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
        "seventeen|eighteen|nineteen|twenty|thirty|forty|"
        "fifty|sixty|seventy|eighty|ninety"
    )

    notice_pattern = re.compile(
        rf"\b(?:\d+|{number_words})\s+"
        r"(?:day|days|month|months|year|years)\b",
        re.IGNORECASE
    )

    for match in notice_pattern.finditer(doc.text):

        entities.append({
            "text": match.group(),
            "label": "NOTICE_PERIOD",
            "description": "Contractual notice period"
        })

    # ----------------------------------------------
    # 4. LEGAL TERMS
    # ----------------------------------------------

    legal_terms = [
        "confidentiality",
        "confidential",
        "terminate",
        "termination",
        "written notice",
        "non-disclosure",
        "indemnity",
        "liability",
        "obligation"
    ]

    for term in legal_terms:

        pattern = re.compile(
            rf"\b{re.escape(term)}\b",
            re.IGNORECASE
        )

        for match in pattern.finditer(doc.text):

            entities.append({
                "text": match.group(),
                "label": "LEGAL_TERM",
                "description": "Legal terminology"
            })

    # ----------------------------------------------
    # REMOVE DUPLICATES
    # ----------------------------------------------

    unique_entities = []
    seen = set()

    for entity in entities:

        key = (
            entity["text"].lower(),
            entity["label"]
        )

        if key not in seen:
            seen.add(key)
            unique_entities.append(entity)

    return unique_entities


# --------------------------------------------------
# MAIN CONTRACT ANALYSIS
# --------------------------------------------------

def analyze_contract(text):

    doc = nlp(text)

    # Tokenization
    tokens = [
        token.text
        for token in doc
        if not token.is_space
    ]

    # Sentence detection
    sentences = [
        sentence.text.strip()
        for sentence in doc.sents
    ]

    # POS tagging
    pos_analysis = []

    for token in doc:

        if not token.is_space:

            pos_analysis.append({
                "word": token.text,
                "pos": token.pos_,
                "description": spacy.explain(token.pos_)
            })

    # Lemmatization
    lemmatization = []

    for token in doc:

        if not token.is_space and not token.is_punct:

            lemmatization.append({
                "word": token.text,
                "lemma": token.lemma_
            })

    # Legal-aware entity extraction
    entities = extract_legal_entities(doc)

    return {
        "tokens": tokens,
        "sentences": sentences,
        "pos": pos_analysis,
        "lemmatization": lemmatization,
        "entities": entities
    }