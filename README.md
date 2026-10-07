# LegalLens – Intelligent Legal Contract Analyzer

LegalLens is a bilingual legal contract analysis system that uses Natural Language Processing (NLP) to analyze legal documents and extract important linguistic, legal, and contractual information.

The system supports **English and Hindi contracts** and provides structured analysis of contract text or uploaded PDF documents.

---

## Features

### Contract Analysis

- English and Hindi contract analysis
- Text-based contract input
- PDF contract upload and text extraction
- Named Entity Recognition (NER)
- Legal entity extraction
- Legal term identification
- Legal clause detection
- Keyword extraction

### Linguistic Analysis

- Tokenization
- Part-of-Speech (POS) analysis
- Lemmatization
- Morphological analysis
- Sentence analysis
- N-gram analysis
- Chunking

### Contract Understanding

- Contract summarization
- Contract simplification
- Important clause identification
- Notice period detection
- Contract comparison
- Downloadable analysis reports

### Contract Risk Assessment

LegalLens provides an **indicative contract risk assessment** using predefined bilingual NLP rules and heuristics.

The system identifies potentially unfavorable contractual conditions such as:

- Automatic renewal
- Long notice periods
- Termination penalties
- Unlimited liability
- Broad indemnity clauses
- Non-compete clauses
- One-sided termination
- Unilateral modification
- Late payment penalties

The detected factors contribute to an overall risk score from **0 to 100**.

| Score | Risk Level |
|------:|------------|
| 0–30 | Low |
| 31–60 | Medium |
| 61–100 | High |

LegalLens also provides recommendations based on detected risk factors.

> **Disclaimer:** The risk assessment is an indicative, project-defined NLP-based heuristic. It does not constitute legal advice or determine whether a contract is legally safe.

---

## Technology Stack

- **Python**
- **Flask**
- **spaCy**
- **Stanza**
- **Natural Language Processing**
- **Jinja2**
- **HTML5**
- **CSS3**
- **PDF text extraction**

---

## NLP Models

### English

```text
spaCy 3.8.16
en_core_web_sm 3.8.0
```

### Hindi

Hindi linguistic analysis uses:

```text
Stanza
```

with tokenization, POS tagging, and lemmatization.

---

## Project Structure

```text
Intelligent-Legal-Contract-Analyzer/
│
├── app.py
├── analyzer.py
├── main_analyzer.py
├── hindi_analyzer.py
├── legal_analyzer.py
├── linguistic_analyzer.py
├── morphology.py
├── preprocessing.py
├── keyword_analyzer.py
├── risk_analyzer.py
├── similarity_analyzer.py
├── summarizer.py
├── simplifier.py
├── pdf_extractor.py
├── report_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── uploads/
│
└── README.md
```

---

## How It Works

```text
                    Contract Input
                          │
                          ▼
                Text / PDF Extraction
                          │
                          ▼
                    Language Selection
                     ┌────┴────┐
                     ▼         ▼
                  English     Hindi
                     │         │
                     └────┬────┘
                          ▼
                    NLP Processing
                          │
                          ▼
             Entity & Legal Term Extraction
                          │
                          ▼
              Clause & Linguistic Analysis
                          │
                          ▼
                  Risk Assessment
                          │
                          ▼
             Summary / Simplification
                          │
                          ▼
                Report Generation
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/avghodekar7/LegalLens.git
```

### 2. Navigate to the project

```bash
cd LegalLens
```

If you are using the existing local folder, you can continue working from it without renaming the folder.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install the English spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 7. Hindi NLP resources

The Hindi analyzer uses Stanza for tokenization, POS tagging, and lemmatization. Ensure the required Hindi Stanza resources are available in the environment before performing Hindi analysis.

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open this address in a web browser.

---

## Demonstration

LegalLens can be demonstrated using realistic English and Hindi employment contracts.

### English Contract

A demonstration contract can contain:

- Employee appointment and salary
- Contract duration
- Automatic renewal
- Notice period
- Termination conditions
- Termination penalty
- Confidentiality
- Non-compete restrictions
- Liability
- Dispute jurisdiction

### Hindi Contract

A Hindi demonstration contract can contain equivalent clauses covering:

- कर्मचारी का पद और वेतन
- अनुबंध की अवधि
- स्वतः नवीनीकरण
- नोटिस अवधि
- रोजगार समाप्ति
- समाप्ति शुल्क
- गोपनीयता
- प्रतिस्पर्धा प्रतिबंध
- दायित्व
- न्यायालय का अधिकार क्षेत्र

This demonstrates that LegalLens performs both contractual analysis and linguistic analysis in English and Hindi.

---

## Example Risk Assessment

For example, a contract containing:

```text
The agreement shall automatically renew.
The employee shall be liable for all losses.
```

may produce:

```text
Risk Score: 35 / 100
Risk Level: Medium

Detected Factors:
- Automatic Renewal
- Unlimited Liability
```

The system then provides recommendations for reviewing the identified contractual conditions.

The same risk assessment functionality can be applied to supported Hindi contractual wording.

---

## Key Workflow

```text
User enters or uploads a contract
              ↓
Selects English or Hindi
              ↓
LegalLens processes the document
              ↓
NLP and linguistic analysis
              ↓
Legal entities and clauses extracted
              ↓
Contract summarized / simplified
              ↓
Risk indicators detected
              ↓
Risk score generated
              ↓
Recommendations displayed
              ↓
Analysis report downloaded
```

---

## Limitations

- Risk assessment is rule-based and indicative.
- Risk detection depends on the wording present in the contract.
- The system does not provide legal advice.
- NLP results may vary depending on the quality, language, and structure of the input.
- Complex legal interpretation may require review by a qualified legal professional.
- The implementation is primarily intended for academic and educational purposes.

---

## Project Purpose

LegalLens is an academic NLP project developed to demonstrate how Natural Language Processing techniques can be applied to legal documents for:

- Information extraction
- Linguistic analysis
- Legal term identification
- Contract understanding
- Clause analysis
- Contract summarization
- Contract simplification
- Preliminary risk identification

The project demonstrates these capabilities through a single bilingual web-based interface supporting **English and Hindi legal contracts**.

---

## Disclaimer

LegalLens is an academic/project implementation intended for educational and research purposes.

The information generated by the system should not be considered professional legal advice. The risk score is an indicative heuristic based on predefined project rules and should not be used as a substitute for review by a qualified legal professional.
