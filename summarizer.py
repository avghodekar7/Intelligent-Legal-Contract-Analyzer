import re
from collections import Counter


# --------------------------------------------------
# SENTENCE SPLITTING
# --------------------------------------------------

def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# --------------------------------------------------
# EXTRACTIVE SUMMARY
# --------------------------------------------------

def generate_summary(text, max_sentences=5):

    sentences = split_sentences(text)

    # Very short text does not need summarization
    if len(sentences) <= max_sentences:

        return {
            "summary": sentences,
            "sentence_scores": [
                {
                    "sentence": sentence,
                    "score": 1
                }
                for sentence in sentences
            ]
        }

    # Legal and contract-related words
    important_words = {
        "agreement",
        "contract",
        "employee",
        "employer",
        "party",
        "parties",
        "payment",
        "salary",
        "compensation",
        "confidentiality",
        "confidential",
        "notice",
        "termination",
        "terminate",
        "liability",
        "liable",
        "indemnity",
        "indemnification",
        "obligation",
        "responsibility",
        "rights",
        "duties",
        "disclosure",
        "damages",
        "invoice",
        "fee",
        "shall",
        "must",
        "required"
    }

    # Count important words in the complete document
    all_words = re.findall(
        r'\b[a-zA-Z]+\b',
        text.lower()
    )

    word_frequency = Counter(
        all_words
    )

    sentence_scores = []

    for sentence in sentences:

        words = re.findall(
            r'\b[a-zA-Z]+\b',
            sentence.lower()
        )

        score = 0

        for word in words:

            if word in important_words:

                # Give more weight to legal words
                score += 2

            elif word_frequency[word] > 1:

                score += 1

        # Slightly reward longer meaningful sentences
        if len(words) >= 8:
            score += 1

        sentence_scores.append({
            "sentence": sentence,
            "score": score
        })

    # Rank sentences by score
    ranked_sentences = sorted(
        sentence_scores,
        key=lambda item: item["score"],
        reverse=True
    )

    # Select top sentences
    selected = ranked_sentences[
        :max_sentences
    ]

    # Restore original document order
    selected_sentences = []

    for sentence in sentences:

        for item in selected:

            if sentence == item["sentence"]:

                selected_sentences.append(
                    sentence
                )

                break

    return {
        "summary": selected_sentences,
        "sentence_scores": sentence_scores
    }


# --------------------------------------------------
# COMPLETE SUMMARY ANALYSIS
# --------------------------------------------------

def analyze_summary(text):

    result = generate_summary(text)

    return {
        "summary": result["summary"],
        "sentence_scores": result["sentence_scores"]
    }