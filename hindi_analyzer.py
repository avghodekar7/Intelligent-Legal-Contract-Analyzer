import re
import stanza
from risk_analyzer import analyze_contract_risk


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


HINDI_NUMBER_WORDS = {
    "शून्य": "0",
    "एक": "1",
    "दो": "2",
    "तीन": "3",
    "चार": "4",
    "पाँच": "5",
    "छह": "6",
    "सात": "7",
    "आठ": "8",
    "नौ": "9",
    "दस": "10",
    "ग्यारह": "11",
    "बारह": "12",
    "तेरह": "13",
    "चौदह": "14",
    "पंद्रह": "15",
    "सोलह": "16",
    "सत्रह": "17",
    "अठारह": "18",
    "उन्नीस": "19",
    "बीस": "20",
    "तीस": "30",
    "चालीस": "40",
    "पचास": "50",
    "साठ": "60",
    "सत्तर": "70",
    "अस्सी": "80",
    "नब्बे": "90",
    "सौ": "100"
}


HINDI_SECTION_TITLES = {
    "renewal": "नवीनीकरण",
    "termination": "समाप्ति",
    "notice": "सूचना अवधि",
    "payment": "वेतन / भुगतान",
    "confidentiality": "गोपनीयता",
    "liability": "दायित्व",
    "indemnity": "क्षतिपूर्ति",
    "non_compete": "प्रतिस्पर्धा प्रतिबंध",
    "penalties": "दंड / शुल्क",
    "governing_law": "लागू कानून",
    "responsibilities": "जिम्मेदारियाँ",
    "other": "अन्य शर्तें"
}


def _normalize_hindi_number_words(text):
    for word, digits in HINDI_NUMBER_WORDS.items():
        text = re.sub(
            rf"(?<![\u0900-\u097F]){word}(?![\u0900-\u097F])",
            digits,
            text
        )

    return text


def _get_hindi_section_title(sentence):
    patterns = [
        ("renewal", r"नवीनीकरण|नवीनीकृत|नवीनीकृत होगा"),
        ("termination", r"समाप्ति|समाप्त कर|समाप्त करेगा|समाप्त किया"),
        ("notice", r"सूचना|नोटिस"),
        ("confidentiality", r"गोपनीय"),
        ("indemnity", r"क्षतिपूर्ति|नुकसान की भरपाई"),
        ("non_compete", r"प्रतिस्पर्धा|प्रतिस्पर्धा नहीं"),
        ("penalties", r"जुर्माना|दंड|शुल्क|जुर्माने"),
        ("governing_law", r"लागू कानून|कानून लागू|कानूनों के अनुसार"),
        ("liability", r"दायित्व|उत्तरदायित्व|उत्तरदायी"),
        ("payment", r"वेतन|भुगतान|राशि|मासिक"),
        ("responsibilities", r"जिम्मेदारी|जिम्मेदारियाँ|कर्तव्य|काम करेगा")
    ]

    for title, pattern in patterns:
        if re.search(pattern, sentence):
            return title

    return "other"


def _simplify_hindi_sentence(sentence):
    text = _normalize_hindi_number_words(sentence.strip())
    if not text:
        return ""

    text = re.sub(
        r"(?:यह\s+)?अनुबंध\s+(?:हर|प्रत्येक)\s+(.+?)\s+की\s+अवधि\s+के\s+लिए\s+"
        r"स्वतः\s+नवीनीकृत\s+होगा",
        r"यह अनुबंध हर \1 बाद अपने आप जारी रहेगा",
        text
    )
    text = re.sub(
        r",?\s*(?:जब तक कि\s+)?(?:कोई भी पक्ष|दोनों में से कोई भी पक्ष)\s+"
        r"(?:वर्तमान अवधि|वर्तमान अनुबंध अवधि|मौजूदा अवधि)\s+की\s+समाप्ति\s+से\s+"
        r"कम से कम\s+(.+?)\s+पहले\s+लिखित\s+सूचना\s+न\s+दे",
        r"। किसी भी पक्ष को अनुबंध रोकने के लिए कम से कम \1 पहले लिखित सूचना देनी होगी",
        text
    )
    text = re.sub(
        r"(?:कंपनी\s+)?(?:कर्मचारी|उसे)\s+को\s+(.+?)\s+मासिक\s+वेतन\s+"
        r"देने\s+के\s+लिए\s+सहमत\s+है",
        r"कंपनी कर्मचारी को \1 मासिक वेतन देगी",
        text
    )
    text = re.sub(
        r"वेतन\s+देने\s+के\s+लिए\s+सहमत\s+है",
        "वेतन देगी",
        text
    )
    text = re.sub(
        r"भुगतान\s+करने\s+के\s+लिए\s+सहमत\s+है",
        "भुगतान करेगी",
        text
    )
    text = re.sub(
        r"(.+?)\s+की\s+गोपनीयता\s+बनाए\s+रखेगा",
        r"\1 को गोपनीय रखेगा",
        text
    )
    text = re.sub(
        r"(.+?)\s+की\s+गोपनीयता\s+बनाए\s+रखनी\s+होगी",
        r"\1 को गोपनीय रखना होगा",
        text
    )
    text = re.sub(
        r"क्षतिपूर्ति\s+करने\s+के\s+लिए\s+सहमत\s+है",
        "नुकसान की भरपाई करेगा",
        text
    )
    text = re.sub(
        r"क्षतिपूर्ति\s+करेगा",
        "नुकसान की भरपाई करेगा",
        text
    )
    text = re.sub(
        r"प्रतिस्पर्धा\s+निषिद्ध\s+होगी",
        "प्रतिस्पर्धा नहीं कर सकता",
        text
    )
    text = re.sub(
        r"दंडनीय\s+होगा",
        "इस पर दंड लगेगा",
        text
    )
    text = re.sub(
        r"के\s+लिए\s+उत्तरदायी\s+होगा",
        "के लिए जिम्मेदार होगा",
        text
    )
    text = re.sub(
        r"इस\s+अनुबंध\s+के\s+संबंध\s+में\s+(.+?)\s+के\s+कानूनों\s+के\s+अधीन\s+होगा",
        r"इस अनुबंध पर \1 के कानून लागू होंगे",
        text
    )
    text = re.sub(
        r"दंड\s+अदा\s+करने\s+के\s+लिए\s+बाध्य\s+होगा",
        "दंड देना होगा",
        text
    )
    text = re.sub(
        r"(.+?)\s+करने\s+के\s+लिए\s+बाध्य\s+होगा",
        r"\1 करना होगा",
        text
    )
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:])", r"\1", text)

    if text and not text.endswith(("।", ".", "!", "?")):
        text += "।"

    return text


def simplify_hindi_contract(sentences):
    sections = []

    for sentence in sentences:
        original = sentence.strip()
        if not original:
            continue

        title_key = _get_hindi_section_title(original)
        title = HINDI_SECTION_TITLES[title_key]
        simplified = _simplify_hindi_sentence(original)
        if not simplified:
            continue

        sections.append({
            "title": title,
            "original": original,
            "simplified": simplified
        })

    return sections


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

    # ----------------------------------------------
    # NLP ANALYSIS
    # ----------------------------------------------

    nlp_results = analyze_hindi_nlp(text)

    # ----------------------------------------------
    # LEGAL TERM DETECTION
    # ----------------------------------------------

    legal_terms = detect_hindi_legal_terms(text)

    # ----------------------------------------------
    # CONTRACT RISK ANALYSIS
    # ----------------------------------------------

    risk_results = analyze_contract_risk(text)

    simplified_sections = simplify_hindi_contract(
        nlp_results["sentences"]
    )

    # ----------------------------------------------
    # FINAL RESULT
    # ----------------------------------------------

    return {
        "tokens": nlp_results["tokens"],
        "sentences": nlp_results["sentences"],
        "legal_terms": legal_terms,
        "morphology": nlp_results["morphology"],
        "simplified_sections": simplified_sections,
        "risk": risk_results
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

    print("\n========== HINDI CONTRACT RISK ==========")

    print(
        f"Risk Score: {result['risk']['score']}/100"
    )

    print(
        f"Risk Level: {result['risk']['level']}"
    )

    print("\nRisk Factors:")

    if result["risk"]["factors"]:

        for factor in result["risk"]["factors"]:

            print(
                f"- {factor['name']} "
                f"(+{factor['points']})"
            )

            print(
                f"  Detected: {factor['matched_text']}"
            )

    else:

        print("- No predefined risk indicators detected.")

    print("\nRecommendations:")

    if result["risk"]["recommendations"]:

        for recommendation in result["risk"]["recommendations"]:

            print(
                f"- {recommendation}"
            )

    else:

        print("- No specific recommendations.")