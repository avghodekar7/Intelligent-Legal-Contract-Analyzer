import re
import stanza


# --------------------------------------------------
# STANZA HINDI NLP PIPELINE
# --------------------------------------------------

nlp = stanza.Pipeline(
    "hi",
    processors="tokenize,pos,lemma",
    download_method=None
)


# --------------------------------------------------
# HINDI LEGAL TERMS
# --------------------------------------------------

HINDI_LEGAL_TERMS = {

    "अनुबंध": "Contract / Agreement",
    "समझौता": "Agreement",
    "भुगतान": "Payment",
    "वेतन": "Salary",
    "गोपनीयता": "Confidentiality",
    "गोपनीय": "Confidential",
    "समाप्त": "Terminate / End",
    "समाप्ति": "Termination",
    "सूचना": "Notice",
    "लिखित सूचना": "Written Notice",
    "दायित्व": "Obligation / Liability",
    "जिम्मेदारी": "Responsibility",
    "क्षतिपूर्ति": "Indemnity",
    "पक्ष": "Party",
    "कर्मचारी": "Employee",
    "कंपनी": "Company",
    "नियोक्ता": "Employer",
    "अधिकार": "Rights",
    "शर्त": "Condition / Term",
    "शर्तें": "Terms and Conditions"
}


# --------------------------------------------------
# HINDI LEGAL TERM DETECTION
# --------------------------------------------------

def detect_hindi_legal_terms(text):

    results = []
    seen = set()

    for term, meaning in HINDI_LEGAL_TERMS.items():

        matches = re.finditer(
            re.escape(term),
            text
        )

        for match in matches:

            key = (term, meaning)

            if key not in seen:

                seen.add(key)

                results.append({
                    "text": term,
                    "label": "LEGAL_TERM",
                    "meaning": meaning
                })

    return results


# --------------------------------------------------
# HINDI NLP ANALYSIS
# --------------------------------------------------

def analyze_hindi_nlp(text):

    doc = nlp(text)

    tokens = []
    sentences = []
    morphology = []

    # ----------------------------------------------
    # SENTENCES
    # ----------------------------------------------

    for sentence in doc.sentences:

        sentences.append(
            sentence.text.strip()
        )

    # ----------------------------------------------
    # TOKENS + MORPHOLOGY
    # ----------------------------------------------

    for sentence in doc.sentences:

        for word in sentence.words:

            # Skip punctuation
            if word.upos == "PUNCT":
                continue

            tokens.append(word.text)

            morphology.append({
                "word": word.text,
                "lemma": word.lemma,
                "pos": word.upos,
                "morphology": word.feats if word.feats else "None"
            })

    return {
        "tokens": tokens,
        "sentences": sentences,
        "morphology": morphology
    }


# --------------------------------------------------
# MAIN HINDI ANALYZER
# --------------------------------------------------

def analyze_hindi(text):

    nlp_results = analyze_hindi_nlp(text)

    legal_terms = detect_hindi_legal_terms(text)

    return {
        "tokens": nlp_results["tokens"],
        "sentences": nlp_results["sentences"],
        "legal_terms": legal_terms,
        "morphology": nlp_results["morphology"]
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    text = """
    यह अनुबंध ABC Technologies कंपनी और कर्मचारी के बीच किया गया है।
    कंपनी कर्मचारी को ₹50,000 मासिक वेतन देने के लिए सहमत है।
    कर्मचारी कंपनी की सभी जानकारी की गोपनीयता बनाए रखेगा।
    कोई भी पक्ष तीस दिन की लिखित सूचना देकर समझौता समाप्त कर सकता है।
    """

    result = analyze_hindi(text)

    print("\n========== HINDI TOKENS ==========")

    print(result["tokens"])

    print("\n========== HINDI SENTENCES ==========")

    for sentence in result["sentences"]:
        print(sentence)

    print("\n========== HINDI LEGAL TERMS ==========")

    for term in result["legal_terms"]:

        print(
            f"{term['text']} → "
            f"{term['meaning']}"
        )

    print("\n========== HINDI MORPHOLOGICAL ANALYSIS ==========")

    for item in result["morphology"]:

        print(
            f"{item['word']} → "
            f"Lemma: {item['lemma']} | "
            f"POS: {item['pos']} | "
            f"Morphology: {item['morphology']}"
        )