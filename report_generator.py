from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def _register_hindi_font():
    candidates = [
        Path(r"C:\Windows\Fonts\Nirmala.ttf"),
        Path(r"C:\Windows\Fonts\NirmalaUI.ttf"),
        Path(r"C:\Windows\Fonts\NotoSansDevanagari-Regular.ttf"),
    ]

    for path in candidates:
        if path.exists():
            try:
                pdfmetrics.registerFont(
                    TTFont("LexiHindi", str(path))
                )
                return "LexiHindi"
            except Exception:
                pass

    return "Helvetica"


def create_simplified_report(text, language, analyzer_results):

    buffer = BytesIO()

    font_name = (
        _register_hindi_font()
        if language == "hindi"
        else "Helvetica"
    )

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="LexiNLP Simplified Contract Report",
        author="LexiNLP",
    )

    styles = getSampleStyleSheet()

    # =========================================================
    # STYLES
    # =========================================================

    title_style = ParagraphStyle(
        "LexiTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#172536"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "LexiSubtitle",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#5f6873"),
        spaceAfter=4,
    )

    heading_style = ParagraphStyle(
        "LexiHeading",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#172536"),
        spaceBefore=10,
        spaceAfter=8,
    )

    section_title_style = ParagraphStyle(
        "LexiSectionTitle",
        parent=styles["Heading3"],
        fontName=font_name,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#B38A48"),
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "LexiBody",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#202733"),
        alignment=TA_LEFT,
        spaceAfter=7,
    )

    original_style = ParagraphStyle(
        "LexiOriginal",
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=3,
    )

    small_style = ParagraphStyle(
        "LexiSmall",
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#5f6873"),
    )

    number_style = ParagraphStyle(
        "LexiNumber",
        parent=body_style,
        fontName=font_name,
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=TA_LEFT,
    )

    story = []

    # =========================================================
    # REPORT HEADER
    # =========================================================

    story.append(
        Paragraph(
            "LexiNLP",
            title_style
        )
    )

    story.append(
        Paragraph(
            "INTELLIGENT LEGAL CONTRACT ANALYZER",
            subtitle_style,
        )
    )

    story.append(Spacer(1, 6 * mm))

    story.append(
        Paragraph(
            "SIMPLIFIED CONTRACT REPORT",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            f"Language: {language.title()}",
            small_style,
        )
    )

    story.append(Spacer(1, 4 * mm))

    # =========================================================
    # PLAIN-LANGUAGE INTRODUCTION
    # =========================================================

    story.append(
        Paragraph(
            "PLAIN-LANGUAGE VIEW",
            section_title_style,
        )
    )

    story.append(
        Paragraph(
            "Key provisions from your contract have been "
            "organized into clear, plain-language sections.",
            body_style,
        )
    )

    # =========================================================
    # SIMPLIFIED PROVISIONS
    # =========================================================

    simplified_sections = analyzer_results.get(
        "simplified_sections",
        []
    )

    if simplified_sections:

        for index, section in enumerate(
            simplified_sections,
            start=1
        ):

            title = str(
                section.get("title", "OTHER TERMS")
            )

            simplified = str(
                section.get("simplified", "")
            )

            original = str(
                section.get("original", "")
            )

            # Number + content layout
            number_table = Table(
                [[
                    Paragraph(
                        f"{index:02d}",
                        number_style,
                    ),
                    [
                        Paragraph(
                            title,
                            section_title_style,
                        ),
                        Paragraph(
                            simplified,
                            body_style,
                        ),
                    ],
                ]],
                colWidths=[
                    14 * mm,
                    150 * mm,
                ],
            )

            number_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, 0),
                        colors.HexColor("#172536"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (0, 0),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (0, 0),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (0, 0),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (0, 0),
                        7,
                    ),
                    (
                        "LEFTPADDING",
                        (1, 0),
                        (1, 0),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (1, 0),
                        (1, 0),
                        2,
                    ),
                    (
                        "TOPPADDING",
                        (1, 0),
                        (1, 0),
                        0,
                    ),
                    (
                        "BOTTOMPADDING",
                        (1, 0),
                        (1, 0),
                        0,
                    ),
                ])
            )

            story.append(number_table)
            story.append(Spacer(1, 4 * mm))

    else:

        story.append(
            Paragraph(
                "No simplified provisions could be generated "
                "from this document.",
                body_style,
            )
        )

    # =========================================================
    # IMPORTANT TERMS
    # =========================================================

    if language == "english":

        keywords = analyzer_results.get(
            "keywords",
            {}
        ).get(
            "keywords",
            []
        )

        if keywords:

            story.append(
                Spacer(1, 5 * mm)
            )

            story.append(
                Paragraph(
                    "IMPORTANT TERMS",
                    heading_style,
                )
            )

            story.append(
                Paragraph(
                    "Frequently occurring meaningful terms "
                    "identified from the contract.",
                    small_style,
                )
            )

            story.append(
                Spacer(1, 3 * mm)
            )

            data = [
                ["Term", "Frequency"]
            ]

            for item in keywords[:8]:

                data.append([
                    str(
                        item.get("word", "")
                    ),
                    str(
                        item.get("frequency", "")
                    ),
                ])

            table = Table(
                data,
                colWidths=[
                    125 * mm,
                    35 * mm
                ],
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#172536"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        font_name,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#deded9"),
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.HexColor("#f8f8f6"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ])
            )

            story.append(table)


    # =========================================================
    # CONTRACT RISK ASSESSMENT
    # =========================================================

    if language == "english":

        risk = analyzer_results.get(
            "risk",
            {}
        )

        risk_score = risk.get(
            "score",
            0
        )

        risk_level = risk.get(
            "level",
            "Low"
        )

        risk_factors = risk.get(
            "factors",
            []
        )

        recommendations = risk.get(
            "recommendations",
            []
        )

        story.append(
            Spacer(1, 7 * mm)
        )

        story.append(
            Paragraph(
                "CONTRACT RISK ASSESSMENT",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                "An indicative assessment of potentially strict "
                "or unfavorable contract clauses identified using "
                "rule-based legal NLP analysis.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 3 * mm)
        )

        # -----------------------------------------------------
        # SCORE TABLE
        # -----------------------------------------------------

        level_colors = {
            "Low": "#3F6B50",
            "Medium": "#9A7028",
            "High": "#9B4D43",
        }

        level_color = level_colors.get(
            risk_level,
            "#172536"
        )

        score_table = Table(
            [[
                Paragraph(
                    f"<b>{risk_score}</b> / 100",
                    body_style,
                ),
                Paragraph(
                    f"<b>{risk_level.upper()} RISK</b>",
                    body_style,
                ),
            ]],
            colWidths=[
                82 * mm,
                78 * mm,
            ],
        )

        score_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F8F8F6"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, 0),
                    colors.HexColor("#172536"),
                ),
                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, 0),
                    colors.HexColor(level_color),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor("#DEDED9"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ])
        )

        story.append(score_table)


        # -----------------------------------------------------
        # RISK FACTORS
        # -----------------------------------------------------

        if risk_factors:

            story.append(
                Spacer(1, 5 * mm)
            )

            story.append(
                Paragraph(
                    "IDENTIFIED RISK FACTORS",
                    section_title_style,
                )
            )

            risk_data = [
                [
                    "Risk Factor",
                    "Detected Term",
                    "Points",
                ]
            ]

            for factor in risk_factors:

                risk_data.append([
                    str(
                        factor.get(
                            "name",
                            ""
                        )
                    ),
                    str(
                        factor.get(
                            "matched_text",
                            ""
                        )
                    ),
                    f"+{factor.get('points', 0)}",
                ])

            risk_table = Table(
                risk_data,
                colWidths=[
                    70 * mm,
                    75 * mm,
                    20 * mm,
                ],
                repeatRows=1,
            )

            risk_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#172536"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        font_name,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8.5,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#DEDED9"),
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.HexColor("#F8F8F6"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ])
            )

            story.append(risk_table)

        else:

            story.append(
                Spacer(1, 4 * mm)
            )

            story.append(
                Paragraph(
                    "No major predefined risk indicators "
                    "were detected.",
                    body_style,
                )
            )


        # -----------------------------------------------------
        # REVIEW SUGGESTIONS
        # -----------------------------------------------------

        if recommendations:

            story.append(
                Spacer(1, 5 * mm)
            )

            story.append(
                Paragraph(
                    "REVIEW SUGGESTIONS",
                    section_title_style,
                )
            )

            for recommendation in recommendations:

                story.append(
                    Paragraph(
                        f"• {recommendation}",
                        body_style,
                    )
                )


        # -----------------------------------------------------
        # RISK DISCLAIMER
        # -----------------------------------------------------

        story.append(
            Spacer(1, 3 * mm)
        )

        story.append(
            Paragraph(
                "<b>Risk assessment disclaimer:</b> "
                "This is an indicative NLP-based assessment "
                "intended to identify potentially important "
                "contract terms. It does not constitute legal "
                "advice or determine whether a contract is "
                "legally safe.",
                small_style,
            )
        )


    else:

        legal_terms = analyzer_results.get(
            "legal_terms",
            []
        )

        if legal_terms:

            story.append(
                Paragraph(
                    "IMPORTANT LEGAL TERMS",
                    heading_style,
                )
            )

            for item in legal_terms[:10]:

                term = item.get(
                    "text",
                    ""
                )

                meaning = item.get(
                    "meaning",
                    ""
                )

                story.append(
                    Paragraph(
                        f"<b>{term}</b> — {meaning}",
                        body_style,
                    )
                )

    # =========================================================
    # FOOTER / DISCLAIMER
    # =========================================================

    story.append(
        Spacer(1, 8 * mm)
    )

    story.append(
        Paragraph(
            "Generated by LexiNLP. This report summarizes "
            "the text processed by the application and is "
            "not legal advice.",
            small_style,
        )
    )

    # =========================================================
    # BUILD PDF
    # =========================================================

    document.build(story)

    buffer.seek(0)

    return buffer