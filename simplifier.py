import re


ENGLISH_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100
}


def _normalize_english_duration_numbers(text):
    number_words = "|".join(ENGLISH_NUMBER_WORDS)
    duration_units = r"(?:business\s+)?(?:days?|weeks?|months?|years?)"
    pattern = rf"\b({number_words})\b(?=(?:\s+|-){duration_units}\b)"

    return re.sub(
        pattern,
        lambda match: str(ENGLISH_NUMBER_WORDS[match.group(1).lower()]),
        text,
        flags=re.IGNORECASE
    )


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

    text = _normalize_english_duration_numbers(original)

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

    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay "
        r"(.+?) a monthly amount of (.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:
        person = match.group(1).strip()
        amount = match.group(2).strip()
        return f"The company will pay {person} {amount} every month."

    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay "
        r"(.+?) (?:the amount of )?(.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:
        person = match.group(1).strip()
        amount = match.group(2).strip()
        return f"The payment to {person} is {amount}."

    rules = [
        (
            r"\bshall automatically renew for successive periods of "
            r"([\w-]+)\s+(days?|weeks?|months?|years?)\b",
            r"will automatically continue for another \1 \2",
        ),
        (
            r"\bautomatically renew for successive periods of "
            r"([\w-]+)\s+(days?|weeks?|months?|years?)\b",
            r"automatically continue for another \1 \2",
        ),
        (
            r"\bunless either party provides written notice at least "
            r"([\w-]+)\s+(days?|weeks?|months?|years?)\s+prior to "
            r"the expiration of the current term\b",
            r". Either party must give written notice at least \1 \2 "
            r"before the current contract ends",
        ),
        (
            r"\bunless either party provides written notice at least "
            r"([\w-]+)\s+(days?|weeks?|months?|years?)\s+before "
            r"the end of the current term\b",
            r". Either party must give written notice at least \1 \2 "
            r"before the current contract ends",
        ),
        (r"\bnon-compete clause\b", "restriction on competing"),
        (r"\bnon compete clause\b", "restriction on competing"),
        (r"\bliquidated damages\b", "agreed compensation for a breach"),
        (
            r"\bprior to the expiration of the current term\b",
            "before the current contract ends",
        ),
        (r"\bsuccessive periods of\b", "another"),
        (r"\bthe expiration of\b", "the end of"),
        (r"\bfor the avoidance of doubt\b", "to be clear"),
        (r"\bnotwithstanding\b", "despite"),
        (r"\bhereinafter\b", "from now on"),
        (r"\baforementioned\b", "mentioned above"),
        (r"\bhereunder\b", "under this agreement"),
        (r"\bthereunder\b", "under it"),
        (r"\bshall be entitled to\b", "can"),
        (r"\bshall be responsible for\b", "is responsible for"),
        (r"\bshall be liable for\b", "is responsible for"),
        (r"\bshall indemnify and hold harmless\b", "must cover the losses of"),
        (r"\bindemnify and hold harmless\b", "cover the losses of"),
        (
            r"\bmaintain confidentiality of (.+?)[.]?$",
            r"keep \1 confidential",
        ),
        (
            r"\bpreserve confidentiality of (.+?)[.]?$",
            r"keep \1 confidential",
        ),
        (
            r"\bconfidentiality of (.+?)[.]?$",
            r"keep \1 confidential",
        ),
        (r"\bshall not compete with\b", "must not compete with"),
        (r"\bnon[- ]competition\b", "agreement not to compete"),
        (r"\bnon[- ]compete\b", "restriction on competing"),
        (r"\bgoverning law\b", "law that applies"),
        (r"\bshall be governed by and construed in accordance with\b",
         "follows"),
        (r"\bshall be governed by\b", "follows"),
        (r"\bin the event that\b", "if"),
        (r"\bin the event of\b", "if"),
        (r"\bfor a period of\b", "for"),
        (r"\bwith respect to\b", "about"),
        (r"\bin the amount of\b", "of"),
        (r"\bno later than\b", "by"),
        (r"\bprior to\b", "before"),
        (r"\bsubsequent to\b", "after"),
        (r"\bcommence\b", "start"),
        (r"\bterminate\b", "end"),
        (r"\btermination\b", "ending"),
        (r"\bremuneration\b", "pay"),
        (r"\bcompensation\b", "pay"),
        (r"\bremit payment\b", "pay"),
        (r"\bmake payment\b", "pay"),
        (r"\bshall\b", "must"),
        (r"\bagrees to\b", "must"),
        (r"\bmay\b", "can"),
        (r"\bhereby\b", ""),
        (r"\bpursuant to\b", "under"),
        (r"\bin accordance with\b", "according to"),
        (r"\bprovide\b", "give"),
        (r"\bproviding\b", "giving"),
    ]

    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:])", r"\1", text)

    if text and not text.endswith((".", "!", "?")):
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

    # Renewal
    if any(word in text for word in [
        "renew",
        "renewal",
        "नवीनीकरण"
    ]):
        return "RENEWAL"

    # Notice period
    if "notice" in text and any(word in text for word in [
        "day",
        "week",
        "month",
        "written",
        "period"
    ]):
        return "NOTICE PERIOD"

    # Termination
    if any(word in text for word in [
        "terminate",
        "termination",
        "end this agreement",
        "ending"
    ]):
        return "TERMINATION"

    categories = [
        (
            "CONFIDENTIALITY",
            ["confidential", "confidentiality"]
        ),
        (
            "INDEMNITY",
            ["indemn", "hold harmless"]
        ),
        (
            "LIABILITY",
            ["liability", "liable", "responsible for any loss"]
        ),
        (
            "NON-COMPETE",
            ["non-compete", "non compete", "non-competition", "compete with"]
        ),
        (
            "PENALTIES / CHARGES",
            ["penalty", "penalties", "fine", "charge", "fee",
             "liquidated damages"]
        ),
        (
            "GOVERNING LAW",
            ["governing law", "governed by", "jurisdiction"]
        ),
        (
            "PAYMENT",
            ["salary", "pay", "payment", "amount", "inr", "rupee",
             "compensation", "wage"]
        ),
        (
            "RESPONSIBILITY",
            ["duty", "obligation", "responsible", "shall", "agrees", "must"]
        )
    ]

    for title, keywords in categories:
        if any(word in text for word in keywords):
            return title

    # Agreement / parties
    if any(word in text for word in [
        "agreement",
        "entered into",
        "between"
    ]):
        return "PARTIES & AGREEMENT"

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

    if isinstance(sentences, str):
        sentences = re.split(r"(?<=[.!?])\s+", sentences.strip())

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

        title = get_section_title(sentence)
        sections.append({
            "title": title,
            "original": sentence,
            "simplified": simplified
        })

    return sections