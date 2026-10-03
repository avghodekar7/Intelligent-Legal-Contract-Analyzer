import re


LEGAL_CLAUSES = {
    "Payment": [
        "pay",
        "payment",
        "salary",
        "amount",
        "fee",
        "compensation",
        "invoice"
    ],

    "Confidentiality": [
        "confidential",
        "confidentiality",
        "non-disclosure",
        "nda",
        "secret information",
        "proprietary information"
    ],

    "Termination": [
        "terminate",
        "termination",
        "cancel",
        "cancellation",
        "end this agreement"
    ],

    "Notice": [
        "notice",
        "written notice",
        "days notice",
        "notice period"
    ],

    "Liability": [
        "liable",
        "liability",
        "damages",
        "loss",
        "indemnity",
        "indemnification"
    ],

    "Obligation": [
        "agrees to",
        "shall",
        "must",
        "required to",
        "responsible for",
        "obligation"
    ]
}


def detect_legal_clauses(text):

    results = {}

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    for clause_type, keywords in LEGAL_CLAUSES.items():

        matched_sentences = []

        for sentence in sentences:

            sentence_lower = sentence.lower()

            matched_keywords = []

            for keyword in keywords:

                if re.search(
                    r"\b" + re.escape(keyword) + r"\b",
                    sentence_lower
                ):
                    matched_keywords.append(keyword)

            if matched_keywords:

                matched_sentences.append({
                    "sentence": sentence.strip(),
                    "keywords": matched_keywords
                })

        if matched_sentences:
            results[clause_type] = matched_sentences

    return results