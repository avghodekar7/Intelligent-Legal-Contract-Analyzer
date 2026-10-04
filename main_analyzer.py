from analyzer import analyze_contract
from legal_analyzer import detect_legal_clauses
from morphology import analyze_morphology
from hindi_analyzer import analyze_hindi
from preprocessing import preprocess_text
from linguistic_analyzer import analyze_linguistics
from keyword_analyzer import analyze_keywords
from summarizer import analyze_summary
from simplifier import simplify_contract

# --------------------------------------------------
# ENGLISH CONTRACT ANALYSIS
# --------------------------------------------------

def analyze_english_contract(text):

    # Basic NLP
    nlp_results = analyze_contract(text)

    # Legal clause detection
    legal_results = detect_legal_clauses(text)

    # Morphological analysis
    morphology_results = analyze_morphology(text)

    # NLP preprocessing
    preprocessing_results = preprocess_text(text)

    # POS, Chunking and N-Grams
    linguistic_results = analyze_linguistics(text)

    # Keyword extraction
    keyword_results = analyze_keywords(text)

    # Contract summarization
    summary_results = analyze_summary(text)

    # Plain-language contract simplification
    simplified_sections = simplify_contract(
        nlp_results["sentences"]
    )

    return {
        "nlp": nlp_results,
        "legal_clauses": legal_results,
        "morphology": morphology_results,
        "preprocessing": preprocessing_results,
        "linguistics": linguistic_results,
        "keywords": keyword_results,
        "summary": summary_results,
        "simplified_sections": simplified_sections
    }


# --------------------------------------------------
# DISPLAY ENGLISH RESULTS
# --------------------------------------------------

def display_english_results(results):

    nlp = results["nlp"]

    print("\n")
    print("=" * 60)
    print("              ENGLISH CONTRACT ANALYSIS")
    print("=" * 60)

    print("\n========== BASIC NLP ANALYSIS ==========")

    print("Number of tokens:", len(nlp["tokens"]))
    print("Number of sentences:", len(nlp["sentences"]))

    print("\n========== SENTENCES ==========")

    for i, sentence in enumerate(nlp["sentences"], start=1):
        print(f"{i}. {sentence}")

    print("\n========== NAMED ENTITIES ==========")

    for entity in nlp["entities"]:

        print(
            f"{entity['text']} → "
            f"{entity['label']} "
            f"({entity['description']})"
        )

    print("\n========== LEGAL CLAUSE ANALYSIS ==========")

    legal = results["legal_clauses"]

    for clause_type, clauses in legal.items():

        print(f"\n--- {clause_type} Clause ---")

        for clause in clauses:

            print("Sentence:", clause["sentence"])

            print(
                "Keywords:",
                ", ".join(clause["keywords"])
            )

    print("\n========== MORPHOLOGICAL ANALYSIS ==========")

    for item in results["morphology"]:

        print(
            f"{item['word']} → "
            f"Lemma: {item['lemma']} | "
            f"POS: {item['pos']} | "
            f"Morphology: {item['morphology']}"
        )

    print("\n========== PREPROCESSING ==========")

    preprocessing = results["preprocessing"]

    print(
        "Script validation:",
        preprocessing["script_validation"]["message"]
    )

    print(
        "Original token count:",
        len(preprocessing["tokens"])
    )

    print(
        "Filtered token count:",
        len(preprocessing["filtered_tokens"])
    )

    print(
        "After stop-word removal:",
        len(preprocessing["stopword_removed"])
    )

    print(
        "Generated words:",
        ", ".join(preprocessing["generated_words"])
    )

    print("\n========== POS TAGGING ==========")

    for item in results["linguistics"]["pos"]:

        print(
            f"{item['word']} → "
            f"{item['pos']} "
            f"({item['description']})"
        )

    print("\n========== CHUNKING ==========")

    for chunk in results["linguistics"]["chunks"]:

        print(
            f"{chunk['text']} → "
            f"Root: {chunk['root']} | "
            f"POS: {chunk['root_pos']}"
        )

    print("\n========== N-GRAM ANALYSIS ==========")

    ngrams = results["linguistics"]["ngrams"]

    print("\n--- Unigrams ---")

    print(
        ", ".join(
            ngrams["unigrams"]
        )
    )

    print("\n--- Bigrams ---")

    print(
        ", ".join(
            ngrams["bigrams"]
        )
    )

    print("\n--- Trigrams ---")

    print(
        ", ".join(
            ngrams["trigrams"]
        )
    )

    print("\n--- Most Frequent Unigrams ---")

    for word, frequency in ngrams["unigram_frequency"].items():

        print(
            f"{word} → {frequency}"
        )

    print("\n--- Most Frequent Bigrams ---")

    for phrase, frequency in ngrams["bigram_frequency"].items():

        print(
            f"{phrase} → {frequency}"
        )

    print("\n--- Most Frequent Trigrams ---")

    for phrase, frequency in ngrams["trigram_frequency"].items():

        print(
            f"{phrase} → {frequency}"
        )


# --------------------------------------------------
# DISPLAY HINDI RESULTS
# --------------------------------------------------

def display_hindi_results(results):

    print("\n")
    print("=" * 60)
    print("                HINDI CONTRACT ANALYSIS")
    print("=" * 60)

    print("\n========== BASIC NLP ANALYSIS ==========")

    print(
        "Number of tokens:",
        len(results["tokens"])
    )

    print(
        "Number of sentences:",
        len(results["sentences"])
    )

    print("\n========== SENTENCES ==========")

    for i, sentence in enumerate(
        results["sentences"],
        start=1
    ):

        print(f"{i}. {sentence}")

    print("\n========== LEGAL TERMS ==========")

    for term in results["legal_terms"]:

        print(
            f"{term['text']} → "
            f"{term['meaning']}"
        )

    print("\n========== MORPHOLOGICAL ANALYSIS ==========")

    for item in results["morphology"]:

        print(
            f"{item['word']} → "
            f"Lemma: {item['lemma']} | "
            f"POS: {item['pos']} | "
            f"Morphology: {item['morphology']}"
        )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    # ----------------------------------------------
    # ENGLISH CONTRACT
    # ----------------------------------------------

    english_file = "data/sample_contract.txt"

    with open(
        english_file,
        "r",
        encoding="utf-8"
    ) as file:

        english_text = file.read()

    english_results = analyze_english_contract(
        english_text
    )

    display_english_results(
        english_results
    )

    # ----------------------------------------------
    # HINDI CONTRACT
    # ----------------------------------------------

    hindi_file = "data/hindi_contract.txt"

    with open(
        hindi_file,
        "r",
        encoding="utf-8"
    ) as file:

        hindi_text = file.read()

    hindi_results = analyze_hindi(
        hindi_text
    )

    display_hindi_results(
        hindi_results
    )


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()