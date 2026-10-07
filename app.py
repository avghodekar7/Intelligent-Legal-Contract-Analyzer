from flask import Flask, render_template, request, send_file
from main_analyzer import analyze_english_contract
from hindi_analyzer import analyze_hindi
from pdf_extractor import extract_text_from_pdf
from similarity_analyzer import compare_contracts
from report_generator import create_simplified_report
import os


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    language = "english"
    text = ""
    filename = ""

    if request.method == "POST":

        language = request.form.get(
            "language",
            "english"
        ).strip().lower()

        input_method = request.form.get(
            "input_method",
            "text"
        ).strip().lower()

        if input_method == "text":
            text = request.form.get(
                "contract_text",
                ""
            )

        elif input_method == "pdf":

            pdf_file = request.files.get(
                "contract_pdf"
            )

            if pdf_file and pdf_file.filename:

                filename = pdf_file.filename

                upload_folder = "uploads"

                os.makedirs(
                    upload_folder,
                    exist_ok=True
                )

                pdf_path = os.path.join(
                    upload_folder,
                    pdf_file.filename
                )

                pdf_file.save(pdf_path)

                text = extract_text_from_pdf(
                    pdf_path
                )

                os.remove(pdf_path)

        if text.strip():

            if language == "hindi":
                results = analyze_hindi(text)

            else:
                language = "english"
                results = analyze_english_contract(text)

    return render_template(
        "index.html",
        results=results,
        language=language,
        text=text,
        filename=filename,
        comparison=None,
        contract1_text="",
        contract2_text=""
    )


@app.route(
    "/compare",
    methods=["POST"]
)
def compare():

    contract1_text = request.form.get(
        "contract1_text",
        ""
    ).strip()

    contract2_text = request.form.get(
        "contract2_text",
        ""
    ).strip()

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    contract1_pdf = request.files.get(
        "contract1_pdf"
    )

    if (
        not contract1_text
        and contract1_pdf
        and contract1_pdf.filename
    ):

        pdf_path = os.path.join(
            upload_folder,
            contract1_pdf.filename
        )

        contract1_pdf.save(pdf_path)

        contract1_text = extract_text_from_pdf(
            pdf_path
        )

        os.remove(pdf_path)

    contract2_pdf = request.files.get(
        "contract2_pdf"
    )

    if (
        not contract2_text
        and contract2_pdf
        and contract2_pdf.filename
    ):

        pdf_path = os.path.join(
            upload_folder,
            contract2_pdf.filename
        )

        contract2_pdf.save(pdf_path)

        contract2_text = extract_text_from_pdf(
            pdf_path
        )

        os.remove(pdf_path)

    comparison = compare_contracts(
        contract1_text,
        contract2_text
    )

    return render_template(
        "index.html",
        results=None,
        language="english",
        text="",
        filename="",
        comparison=comparison,
        contract1_text=contract1_text,
        contract2_text=contract2_text
    )


@app.route(
    "/download-report",
    methods=["POST"]
)
def download_report():

    text = request.form.get(
        "contract_text",
        ""
    ).strip()

    language = request.form.get(
        "language",
        "english"
    ).strip().lower()

    if not text:
        return "No contract text is available for the report.", 400

    if language == "hindi":
        results = analyze_hindi(text)
    else:
        language = "english"
        results = analyze_english_contract(text)

    report = create_simplified_report(
        text,
        language,
        results
    )

    return send_file(
        report,
        as_attachment=True,
        download_name="LegalLens_Simplified_Contract_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)