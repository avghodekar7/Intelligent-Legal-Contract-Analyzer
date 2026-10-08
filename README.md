# ⚖️ LegalLens

### Intelligent Legal Contract Analyzer

LegalLens is an NLP-based legal contract analysis system that helps users understand English and Hindi contracts through automated entity extraction, clause analysis, summarization, simplification, and rule-based risk assessment.

---

## 📖 Overview

Legal contracts often contain complex legal terminology and lengthy clauses that can be difficult for non-legal users to understand.

**LegalLens** analyzes uploaded contracts and presents the important information in a structured and easier-to-understand format.

The system supports:

- English and Hindi contract analysis
- Named Entity Recognition (NER)
- Legal clause and keyword analysis
- Contract summarization
- Rule-based contract simplification
- Contract risk assessment
- PDF report generation
- Web-based analysis interface

> **Note:** LegalLens is an academic project and provides indicative analysis only. It does not replace professional legal advice.

---

## ✨ Key Features

### 🔍 Contract Analysis

The system processes the contract and extracts important information such as:

- Organizations
- Persons
- Dates
- Monetary values
- Legal terms
- Notice periods
- Contract-related clauses

The system supports both **English and Hindi** contract content.

---

### ⚖️ Risk Assessment

LegalLens uses a transparent, rule-based risk analysis system to identify potentially concerning contractual conditions.

The current risk factors include:

- Automatic Renewal
- Long Notice Period
- Termination Penalty
- Unlimited Liability
- Broad Indemnity
- Non-Compete Clause
- One-Sided Termination
- Unilateral Modification
- Late Payment Penalty

The system calculates a score from **0–100**:

| Score | Risk Level |
|------:|------------|
| 0–30 | Low |
| 31–60 | Medium |
| 61–100 | High |

The result also shows the factors that contributed to the risk score.

---

### 📝 Summarization

LegalLens generates a concise representation of the analyzed contract while retaining important information identified by the system.

This helps users quickly understand the main contents of a lengthy contract.

---

### 💡 Contract Simplification

The system converts complicated contractual statements into more understandable language using **rule-based transformations**.

Simplification is available for:

- English
- Hindi

Related clauses with the same category or section title are **grouped together in the interface**, making connected contractual conditions easier to review.

The simplification module does not depend on an external generative-AI API.

---

### 📄 PDF Reports

Users can generate a simplified contract analysis report containing the processed results.

The report can include:

- Contract information
- Extracted entities
- Summary
- Simplified clauses
- Risk assessment
- Risk factors
- Analysis information

---

## 🧠 NLP Pipeline

The overall processing pipeline is:

```text
Contract Upload
      ↓
PDF / Text Extraction
      ↓
Text Preprocessing
      ↓
Language Detection / Routing
      ↓
NLP Analysis
      ↓
Entity & Clause Extraction
      ↓
Summarization
      ↓
Simplification
      ↓
Risk Assessment
      ↓
Results Dashboard
      ↓
PDF Report
```

For English text, LegalLens uses **spaCy** for NLP processing.

For Hindi text, the system uses **Stanza** and project-defined Hindi processing rules.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Web Framework | Flask |
| English NLP | spaCy |
| Hindi NLP | Stanza |
| PDF Processing | Python PDF processing libraries |
| Frontend | HTML, CSS, JavaScript |
| Report Generation | ReportLab |
| Version Control | Git & GitHub |

### NLP Model

English NLP uses:

```text
spaCy 3.8.x
en_core_web_sm 3.8.0
```

---

## 📁 Project Structure

```text
LegalLens/
│
├── app.py
├── analyzer.py
├── main_analyzer.py
├── hindi_analyzer.py
├── legal_analyzer.py
├── linguistic_analyzer.py
├── keyword_analyzer.py
├── morphology.py
├── preprocessing.py
├── pdf_extractor.py
├── summarizer.py
├── simplifier.py
├── risk_analyzer.py
├── similarity_analyzer.py
├── report_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/avghodekar7/LegalLens.git
cd LegalLens
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

**Activate it on Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install the English spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Example Analysis

LegalLens can analyze contracts containing information such as:

- Parties involved
- Contract start and end dates
- Salary or payment information
- Notice periods
- Termination conditions
- Confidentiality clauses
- Non-compete clauses
- Liability conditions
- Renewal conditions
- Jurisdiction

The system then presents the extracted information, simplified clauses, summary, and indicative risk assessment through the web interface.

---

## 📊 Evaluation

Since LegalLens uses a modular NLP pipeline and **rule-based risk, summarization, and simplification components**, it is not presented as a supervised classification model.

Therefore, traditional model-training metrics such as:

- Accuracy
- Precision
- Recall
- F1-score

are not reported as training results.

The current implementation is evaluated functionally and qualitatively based on:

- Correct entity extraction
- Representative risk detection
- English and Hindi routing
- Contract summarization
- Grouped contract simplification
- PDF report generation
- Overall system functionality

---

## ⚠️ Limitations

- Risk assessment is based on predefined rules and patterns.
- The system does not provide legal advice.
- Complex legal interpretations may require professional legal review.
- The current Hindi analysis supports project-defined language patterns and terminology.
- Results may vary depending on the structure and wording of the contract.

---

## 🔮 Future Scope

Possible future improvements include:

- Expanded legal clause detection
- Additional Indian languages
- Improved semantic similarity analysis
- More advanced legal-domain NLP models
- OCR support for scanned contracts
- Improved clause comparison
- Larger legal-domain datasets
- More comprehensive risk rules

---

## ⚠️ Disclaimer

LegalLens is an academic and informational tool.

The risk scores, summaries, simplifications, and extracted information are generated for analysis and awareness purposes only. They should **not be considered legal advice** or used as a substitute for consultation with a qualified legal professional.

Always consult a qualified lawyer before making important contractual decisions.
