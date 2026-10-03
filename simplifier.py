import re


def simplify_sentence(sentence):
    """
    Convert common legal wording into simpler language.
    The function preserves important names, dates and amounts.
    """

    original = sentence.strip()

    if not original:
        return ""

    text = original

    # Agreement / parties
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
            f"{party1} and {party2} are entering into this agreement "
            f"on {date}."
        )

    # Monthly salary / payment
    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay (.+?) a monthly amount of (.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:
        person = match.group(1).strip()
        amount = match.group(2).strip()

        return f"The company will pay {person} {amount} every month."

    # General payment
    match = re.search(
        r"(?:agrees|agreed|shall agree) to pay (.+?) (?:the amount of )?(.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if match:
        person = match.group(1).strip()
        amount = match.group(2).strip()

        return f"The payment to {person} is {amount}."

    # Confidentiality
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

        simplified = re.sub(
            r"company information",
            "company information confidential",
            simplified,
            flags=re.IGNORECASE
        )

        if not simplified.endswith("."):
            simplified += "."

        return simplified

    # Termination
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

        simplified = re.sub(
            r"written notice",
            "written notice",
            simplified,
            flags=re.IGNORECASE
        )

        return simplified

    # Shall → must
    text = re.sub(
        r"\bshall\b",
        "must",
        text,
        flags=re.IGNORECASE
    )

    # Agrees to → must
    text = re.sub(
        r"\bagrees to\b",
        "must",
        text,
        flags=re.IGNORECASE
    )

    # May → can
    text = re.sub(
        r"\bmay\b",
        "can",
        text,
        flags=re.IGNORECASE
    )

    # Hereby → now / simply remove it
    text = re.sub(
        r"\bhereby\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Commence → start
    text = re.sub(
        r"\bcommence\b",
        "start",
        text,
        flags=re.IGNORECASE
    )

    # Prior → before
    text = re.sub(
        r"\bprior\b",
        "before",
        text,
        flags=re.IGNORECASE
    )

    # Pursuant to → under
    text = re.sub(
        r"\bpursuant to\b",
        "under",
        text,
        flags=re.IGNORECASE
    )

    # In accordance with → according to
    text = re.sub(
        r"\bin accordance with\b",
        "according to",
        text,
        flags=re.IGNORECASE
    )

    # Make whitespace clean
    text = re.sub(r"\s+", " ", text).strip()

    if text and not text.endswith("."):
        text += "."

    return text


def get_section_title(sentence):
    """
    Give each sentence a meaningful legal category.
    """

    text = sentence.lower()

    if any(word in text for word in [
        "agreement",
        "entered into",
        "between"
    ]):
        return "PARTIES & AGREEMENT"

    if any(word in text for word in [
        "salary",
        "pay",
        "payment",
        "amount",
        "inr",
        "rupee"
    ]):
        return "PAYMENT"

    if any(word in text for word in [
        "confidential",
        "confidentiality"
    ]):
        return "CONFIDENTIALITY"

    if any(word in text for word in [
        "terminate",
        "termination",
        "notice"
    ]):
        return "TERMINATION"

    if any(word in text for word in [
        "duty",
        "obligation",
        "responsible",
        "shall",
        "agrees"
    ]):
        return "RESPONSIBILITY"

    if any(word in text for word in [
        "date",
        "dated",
        "effective"
    ]):
        return "DATE / EFFECTIVE PERIOD"

    return "OTHER TERMS"


def simplify_contract(sentences):
    """
    Create structured plain-language sections.
    """

    sections = []

    for sentence in sentences:

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