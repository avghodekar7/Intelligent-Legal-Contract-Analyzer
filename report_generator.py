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

    title_style = ParagraphStyle(
        "LexiTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#172536"),
        spaceAfter=8,
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

    small_style = ParagraphStyle(
        "LexiSmall",
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#5f6873"),
    )

    story = []

    story.append(Paragraph("LexiNLP", title_style))
    story.append(Paragraph(
        "INTELLIGENT LEGAL CONTRACT ANALYZER",
        small_style,
    ))
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("SIMPLIFIED CONTRACT REPORT", heading_style))
    story.append(Paragraph(
        f"Language: {language.title()}",
        small_style,
    ))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("PLAIN-LANGUAGE SUMMARY", heading_style))

    if language == "english":
        summary = analyzer_results.get("summary", {}).get("summary", [])
    else:
        summary = analyzer_results.get("sentences", [])

    if summary:
        for index, sentence in enumerate(summary, start=1):
            story.append(
                Paragraph(
                    f"<b>{index:02d}</b> &nbsp; {sentence}",
                    body_style,
                )
            )
    else:
        story.append(
            Paragraph(
                "No simplified summary could be generated from this document.",
                body_style,
            )
        )

    if language == "english":
        keywords = analyzer_results.get("keywords", {}).get("keywords", [])

        if keywords:
            story.append(Paragraph("IMPORTANT TERMS", heading_style))

            data = [["Term", "Frequency"]]
            for item in keywords[:10]:
                data.append([
                    str(item.get("word", "")),
                    str(item.get("frequency", "")),
                ])

            table = Table(data, colWidths=[125 * mm, 35 * mm])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172536")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#deded9")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8f8f6")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story.append(table)

    else:
        legal_terms = analyzer_results.get("legal_terms", [])
        if legal_terms:
            story.append(Paragraph("IMPORTANT LEGAL TERMS", heading_style))
            for item in legal_terms[:10]:
                term = item.get("text", "")
                meaning = item.get("meaning", "")
                story.append(
                    Paragraph(
                        f"<b>{term}</b> — {meaning}",
                        body_style,
                    )
                )

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "Generated by LexiNLP. This report summarizes the text processed by the application and is not legal advice.",
        small_style,
    ))

    document.build(story)
    buffer.seek(0)
    return buffer