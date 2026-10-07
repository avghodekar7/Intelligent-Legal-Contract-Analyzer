import re


# ==================================================
# RISK CONFIGURATION
# ==================================================

RISK_RULES = {

    "Automatic Renewal": {
        "keywords": {
            "english": [
                "renew",
                "renewal",
                "automatically",
                "auto-renew"
            ],
            "hindi": [
                "नवीनीकरण",
                "नवीनीकृत",
                "स्वचालित",
                "स्वतः"
            ]
        },
        "points": 10
    },

    "Termination Penalty": {
        "keywords": {
            "english": [
                "termination",
                "terminate",
                "penalty",
                "fee",
                "charge",
                "liquidated damages"
            ],
            "hindi": [
                "समाप्ति",
                "समाप्त",
                "दंड",
                "जुर्माना",
                "शुल्क",
                "क्षतिपूर्ति"
            ]
        },
        "points": 20
    },

    "Unlimited Liability": {
        "keywords": {
            "english": [
                "unlimited liability",
                "unlimited liable",
                "liable for all",
                "liable for any and all",
                "all losses",
                "all damages"
            ],
            "hindi": [
                "असीमित दायित्व",
                "असीमित जिम्मेदारी",
                "सभी हानियों",
                "सभी क्षतियों",
                "सभी नुकसान",
                "उत्तरदायी"
            ]
        },
        "points": 25
    },

    "Broad Indemnity": {
        "keywords": {
            "english": [
                "indemnify",
                "indemnification",
                "hold harmless"
            ],
            "hindi": [
                "क्षतिपूर्ति",
                "क्षतिपूर्ति करेगा",
                "हानि से मुक्त"
            ]
        },
        "points": 15
    },

    "Non-Compete Clause": {
        "keywords": {
            "english": [
                "non-compete",
                "non compete",
                "shall not compete",
                "competing"
            ],
            "hindi": [
                "प्रतिस्पर्धा",
                "प्रतिस्पर्धा नहीं",
                "प्रतिस्पर्धा प्रतिबंध",
                "प्रतियोगिता"
            ]
        },
        "points": 15
    },

    "One-Sided Termination": {
        "keywords": {
            "english": [
                "sole discretion",
                "terminate at any time",
                "without cause",
                "without notice"
            ],
            "hindi": [
                "एकपक्षीय समाप्ति",
                "एकतरफा समाप्ति",
                "बिना सूचना समाप्त",
                "किसी भी समय समाप्त"
            ]
        },
        "points": 15
    },

    "Unilateral Modification": {
        "keywords": {
            "english": [
                "modify at any time",
                "modify the terms",
                "change the terms",
                "without consent"
            ],
            "hindi": [
                "एकतरफा संशोधन",
                "एकतरफा परिवर्तन",
                "बिना सहमति",
                "शर्तों में परिवर्तन"
            ]
        },
        "points": 15
    },

    "Late Payment Penalty": {
        "keywords": {
            "english": [
                "late payment",
                "overdue payment",
                "interest on overdue",
                "interest on late payment"
            ],
            "hindi": [
                "देर से भुगतान",
                "विलंबित भुगतान",
                "बकाया भुगतान",
                "विलंबित भुगतान ब्याज"
            ]
        },
        "points": 10
    }
}


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def find_keyword(text, keywords):
    """
    Find the first relevant keyword/concept
    present in the contract text.
    """

    for keyword in keywords:

        pattern = re.escape(keyword)

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return None


def contains_any(text, keywords):
    """
    Check whether at least one keyword is present.
    """

    return find_keyword(text, keywords) is not None


# ==================================================
# AUTOMATIC RENEWAL
# ==================================================

def detect_automatic_renewal(text):

    english = RISK_RULES["Automatic Renewal"]["keywords"]["english"]
    hindi = RISK_RULES["Automatic Renewal"]["keywords"]["hindi"]

    # Strong combinations
    if (
        contains_any(text, ["automatic", "automatically", "auto-renew"])
        and contains_any(text, ["renew", "renewal"])
    ):
        return find_keyword(
            text,
            ["automatically", "auto-renew", "automatic"]
        )

    if (
        contains_any(text, ["स्वचालित", "स्वतः"])
        and contains_any(text, ["नवीनीकरण", "नवीनीकृत"])
    ):
        return find_keyword(
            text,
            ["स्वचालित", "स्वतः"]
        )

    # Explicit renewal phrases
    return find_keyword(text, english + hindi)


# ==================================================
# TERMINATION PENALTY
# ==================================================

def detect_termination_penalty(text):

    if contains_any(
        text,
        [
            "termination penalty",
            "termination fee",
            "termination charge",
            "penalty for termination",
            "liquidated damages"
        ]
    ):
        return find_keyword(
            text,
            [
                "termination penalty",
                "termination fee",
                "termination charge",
                "penalty for termination",
                "liquidated damages"
            ]
        )

    if (
        contains_any(
            text,
            ["समाप्ति", "समाप्त"]
        )
        and contains_any(
            text,
            ["दंड", "जुर्माना", "शुल्क"]
        )
    ):
        return find_keyword(
            text,
            ["दंड", "जुर्माना", "शुल्क"]
        )

    return None


# ==================================================
# UNLIMITED LIABILITY
# ==================================================

def detect_unlimited_liability(text):

    english_patterns = [
        "unlimited liability",
        "unlimited liable",
        "liable for all",
        "liable for any and all",
        "all losses",
        "all damages"
    ]

    hindi_patterns = [
        "असीमित दायित्व",
        "असीमित जिम्मेदारी",
        "सभी हानियों",
        "सभी क्षतियों",
        "सभी नुकसान"
    ]

    match = find_keyword(
        text,
        english_patterns + hindi_patterns
    )

    if match:
        return match

    # Concept combination for Hindi
    if (
        contains_any(
            text,
            ["उत्तरदायी", "जिम्मेदारी", "दायित्व"]
        )
        and contains_any(
            text,
            ["सभी", "हानि", "क्षति", "नुकसान"]
        )
    ):
        return " ".join(
            [
                word
                for word in [
                    "सभी",
                    "हानि",
                    "उत्तरदायी"
                ]
                if word in text
            ]
        )

    return None


# ==================================================
# BROAD INDEMNITY
# ==================================================

def detect_broad_indemnity(text):

    match = find_keyword(
        text,
        [
            "indemnify",
            "indemnification",
            "hold harmless",
            "क्षतिपूर्ति",
            "हानि से मुक्त"
        ]
    )

    if match:
        return match

    return None


# ==================================================
# NON-COMPETE
# ==================================================

def detect_non_compete(text):

    match = find_keyword(
        text,
        [
            "non-compete",
            "non compete",
            "shall not compete",
            "प्रतिस्पर्धा प्रतिबंध",
            "प्रतिस्पर्धा नहीं"
        ]
    )

    if match:
        return match

    return None


# ==================================================
# ONE-SIDED TERMINATION
# ==================================================

def detect_one_sided_termination(text):

    match = find_keyword(
        text,
        [
            "sole discretion",
            "terminate at any time",
            "without cause",
            "terminate without notice",
            "एकपक्षीय समाप्ति",
            "एकतरफा समाप्ति",
            "बिना सूचना समाप्त",
            "किसी भी समय समाप्त"
        ]
    )

    if match:
        return match

    return None


# ==================================================
# UNILATERAL MODIFICATION
# ==================================================

def detect_unilateral_modification(text):

    match = find_keyword(
        text,
        [
            "modify at any time",
            "modify the terms",
            "change the terms",
            "without consent",
            "एकतरफा संशोधन",
            "एकतरफा परिवर्तन",
            "बिना सहमति",
            "शर्तों में परिवर्तन"
        ]
    )

    if match:
        return match

    return None


# ==================================================
# LATE PAYMENT PENALTY
# ==================================================

def detect_late_payment_penalty(text):

    match = find_keyword(
        text,
        [
            "late payment",
            "overdue payment",
            "interest on overdue",
            "interest on late payment",
            "देर से भुगतान",
            "विलंबित भुगतान",
            "बकाया भुगतान",
            "विलंबित भुगतान ब्याज"
        ]
    )

    if match:
        return match

    return None


# ==================================================
# LONG NOTICE PERIOD
# ==================================================

def detect_long_notice_period(text):

    # ----------------------------------------------
    # English numeric periods
    # ----------------------------------------------

    english_pattern = re.compile(
        r"\b(\d+)\s*(day|days|month|months|year|years)\b",
        re.IGNORECASE
    )

    matches = english_pattern.findall(text)

    for number, unit in matches:

        number = int(number)

        if "month" in unit.lower():
            days = number * 30

        elif "year" in unit.lower():
            days = number * 365

        else:
            days = number

        if days >= 90:

            return {
                "name": "Long Notice Period",
                "points": 15,
                "matched_text": f"{number} {unit}"
            }

    # ----------------------------------------------
    # Hindi numeric periods
    # ----------------------------------------------

    hindi_pattern = re.compile(
        r"(\d+)\s*(दिन|महीना|महीने|माह|वर्ष|साल)",
        re.IGNORECASE
    )

    matches = hindi_pattern.findall(text)

    for number, unit in matches:

        number = int(number)

        if unit in ["महीना", "महीने", "माह"]:
            days = number * 30

        elif unit in ["वर्ष", "साल"]:
            days = number * 365

        else:
            days = number

        if days >= 90:

            return {
                "name": "Long Notice Period",
                "points": 15,
                "matched_text": f"{number} {unit}"
            }

    return None


# ==================================================
# RISK DETECTION MAP
# ==================================================

DETECTORS = {

    "Automatic Renewal": detect_automatic_renewal,

    "Termination Penalty": detect_termination_penalty,

    "Unlimited Liability": detect_unlimited_liability,

    "Broad Indemnity": detect_broad_indemnity,

    "Non-Compete Clause": detect_non_compete,

    "One-Sided Termination": detect_one_sided_termination,

    "Unilateral Modification": detect_unilateral_modification,

    "Late Payment Penalty": detect_late_payment_penalty
}


# ==================================================
# RECOMMENDATIONS
# ==================================================

RECOMMENDATIONS = {

    "Automatic Renewal":
        "Review the automatic renewal conditions and notice requirements.",

    "Termination Penalty":
        "Review the financial consequences of terminating the contract.",

    "Unlimited Liability":
        "Review whether liability is limited or capped.",

    "Broad Indemnity":
        "Review the scope of indemnification obligations.",

    "Non-Compete Clause":
        "Review the duration and scope of the non-compete restriction.",

    "One-Sided Termination":
        "Review whether termination rights are balanced between parties.",

    "Unilateral Modification":
        "Review whether one party can modify the agreement without consent.",

    "Late Payment Penalty":
        "Review the interest or penalties associated with late payments.",

    "Long Notice Period":
        "Review whether the notice period is reasonable for the agreement."
}


# ==================================================
# MAIN CONTRACT RISK ANALYSIS
# ==================================================

def analyze_contract_risk(text):

    risk_factors = []
    score = 0

    # ----------------------------------------------
    # Detect risk categories
    # ----------------------------------------------

    for risk_name, detector in DETECTORS.items():

        matched_text = detector(text)

        if matched_text:

            points = RISK_RULES[risk_name]["points"]

            risk_factors.append({
                "name": risk_name,
                "points": points,
                "matched_text": matched_text
            })

            score += points

    # ----------------------------------------------
    # Long notice period
    # ----------------------------------------------

    notice_risk = detect_long_notice_period(text)

    if notice_risk:

        risk_factors.append(notice_risk)

        score += notice_risk["points"]

    # ----------------------------------------------
    # Maximum score
    # ----------------------------------------------

    score = min(score, 100)

    # ----------------------------------------------
    # Risk level
    # ----------------------------------------------

    if score <= 30:

        level = "Low"

    elif score <= 60:

        level = "Medium"

    else:

        level = "High"

    # ----------------------------------------------
    # Recommendations
    # ----------------------------------------------

    recommendations = []

    for factor in risk_factors:

        recommendation = RECOMMENDATIONS.get(
            factor["name"]
        )

        if recommendation:

            recommendations.append(
                recommendation
            )

    # ----------------------------------------------
    # Final result
    # ----------------------------------------------

    return {
        "score": score,
        "level": level,
        "factors": risk_factors,
        "recommendations": recommendations
    }