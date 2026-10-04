import re


# ============================================================
# SENTENCE CLEANUP
# ============================================================

def merge_sentence_fragments(sentences):
    """
    Merge sentence fragments incorrectly created by NLP sentence
    splitting, especially abbreviations such as Pvt. Ltd.
    """

    merged = []

    # Common abbreviations that should NOT end a sentence
    abbreviations = {
        "pvt.",
        "ltd.",
        "mr.",
        "mrs.",
        "ms.",
        "dr.",
        "prof.",
        "inc.",
        "corp.",
        "co.",
        "no.",
        "etc.",
        "e.g.",
        "i.e."
    }

    i = 0

    while i < len(sentences):

        current = sentences[i].strip()

        if not current:
            i += 1
            continue

        # ----------------------------------------------------
        # Join fragments such as:
        #
        # "ABC Technologies Pvt."
        # "Ltd."
        #
        # into:
        #
        # "ABC Technologies Pvt. Ltd."
        # ----------------------------------------------------

        while i + 1 < len(sentences):

            next_sentence = sentences[i + 1].strip()

            if not next_sentence:
                i += 1
                continue

            last_word = current.split()[-1].lower()

            # Current sentence ends with an abbreviation
            if last_word in abbreviations:
                current = current + " " + next_sentence
                i += 1
                continue

            # Next sentence begins with a lowercase word.
            # This usually indicates that the previous sentence
            # was incorrectly split.
            if next_sentence[0].islower():
                current = current + " " + next_sentence
                i += 1
                continue

            break

        merged.append(current)

        i += 1

    return merged


# ============================================================
# SENTENCE SIMPLIFICATION
# ============================================================

def simplify_sentence(sentence):
    """
    Convert common legal wording into simpler language.
    Important names, dates and amounts are preserved.
    """

    original = sentence.strip()

    if not original:
        return ""

    text = original

    # --------------------------------------------------------
    # AGREEMENT / PARTIES
    # --------------------------------------------------------

    match = re.search(
        r"This Agreement is entered into between (.+?) and (.+?) on (.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:

        party1 = match.group(1).strip()
        party2 = match.group(2).strip()
        date = match.group(3).strip()

        return (
            f"{party1} and {party2} are entering into this "
            f"agreement on {date}."
        )

    # --------------------------------------------------------
    # MONTHLY SALARY / PAYMENT
    # --------------------------------------------------------

    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay "
        r"(.+?) a monthly amount of (.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:

        person = match.group(1).strip()
        amount = match.group(2).strip()

        return (
            f"The company will pay {person} "
            f"{amount} every month."
        )

    # --------------------------------------------------------
    # GENERAL PAYMENT
    # --------------------------------------------------------

    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay "
        r"(.+?) (?:the amount of )?(.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:

        person = match.group(1).strip()
        amount = match.group(2).strip()

        return (
            f"The payment to {person} is {amount}."
        )

    # --------------------------------------------------------
    # CONFIDENTIALITY
    # --------------------------------------------------------

    if re.search(
        r"confidential|confidentiality",
        text,
        re.IGNORECASE
    ):

        simplified = re.sub(
            r"the employee agrees to maintain confidentiality of",
            "The employee must keep",
            text,
            flags=re.IGNORECASE
        )

        simplified = re.sub(
            r"maintain confidentiality of",
            "keep",
            simplified,
            flags=re.IGNORECASE
        )

        # Avoid creating awkward duplicate wording
        simplified = re.sub(
            r"company information\.?$",
            "company information confidential.",
            simplified,
            flags=re.IGNORECASE
        )

        if not simplified.endswith("."):
            simplified += "."

        return simplified

    # --------------------------------------------------------
    # TERMINATION
    # --------------------------------------------------------

    if re.search(
        r"terminate|termination",
        text,
        re.IGNORECASE
    ):

        simplified = text

        simplified = re.sub(
            r"Either party may terminate",
            "Either side can end",
            simplified,
            flags=re.IGNORECASE
        )

        simplified = re.sub(
            r"this agreement",
            "the agreement",
            simplified,
            flags=re.IGNORECASE
        )

        simplified = re.sub(
            r"by providing",
            "by giving",
            simplified,
            flags=re.IGNORECASE
        )

        if not simplified.endswith("."):
            simplified += "."

        return simplified

    # --------------------------------------------------------
    # COMMON LEGAL WORDING
    # --------------------------------------------------------

    text = re.sub(
        r"\bshall\b",
        "must",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bagrees to\b",
        "must",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bmay\b",
        "can",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bhereby\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bcommence\b",
        "start",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bprior\b",
        "before",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bpursuant to\b",
        "under",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bin accordance with\b",
        "according to",
        text,
        flags=re.IGNORECASE
    )

    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    if text and not text.endswith("."):
        text += "."

    return text


# ============================================================
# SECTION TITLE
# ============================================================

def get_section_title(sentence):
    """
    Assign a meaningful legal category to a contract provision.
    """

    text = sentence.lower()

    # Agreement / parties
    if any(word in text for word in [
        "agreement",
        "entered into",
        "between"
    ]):
        return "PARTIES & AGREEMENT"

    # Payment
    if any(word in text for word in [
        "salary",
        "pay",
        "payment",
        "amount",
        "inr",
        "rupee",
        "compensation",
        "wage"
    ]):
        return "PAYMENT"

    # Confidentiality
    if any(word in text for word in [
        "confidential",
        "confidentiality"
    ]):
        return "CONFIDENTIALITY"

    # Termination
    if any(word in text for word in [
        "terminate",
        "termination",
        "notice"
    ]):
        return "TERMINATION"

    # Responsibilities
    if any(word in text for word in [
        "duty",
        "obligation",
        "responsible",
        "shall",
        "agrees"
    ]):
        return "RESPONSIBILITY"

    # Dates
    if any(word in text for word in [
        "date",
        "dated",
        "effective"
    ]):
        return "DATE / EFFECTIVE PERIOD"

    return "OTHER TERMS"


# ============================================================
# CONTRACT SIMPLIFICATION
# ============================================================

def simplify_contract(sentences):
    """
    Convert contract sentences into structured,
    plain-language legal provisions.
    """

    # First fix incorrect sentence splitting
    cleaned_sentences = merge_sentence_fragments(sentences)

    sections = []

    for sentence in cleaned_sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        simplified = simplify_sentence(sentence)

        if not simplified:
            continue

        sections.append({
            "title": get_section_title(sentence),
            "original": sentence,
            "simplified": simplified
        })

    return sections