# LegalLens -- Intelligent Legal Contract Analyzer

LegalLens is a bilingual legal contract analysis system that uses Natural
Language Processing (NLP) to analyze legal documents and extract
important linguistic, legal, and contractual information.

The system supports both **English and Hindi contracts** and provides a
structured analysis of contract text or uploaded PDF documents.

------------------------------------------------------------------------

## Features

### Contract Analysis

-   English and Hindi contract analysis
-   Text-based contract input
-   PDF contract upload and text extraction
-   Named Entity Recognition (NER)
-   Legal entity extraction
-   Legal term identification
-   Legal clause detection
-   Keyword extraction

### Linguistic Analysis

-   Tokenization
-   Part-of-Speech (POS) analysis
-   Lemmatization
-   Morphological analysis
-   Sentence analysis
-   N-gram analysis
-   Chunking

### Contract Understanding

-   Contract summarization
-   Contract simplification
-   Important clause identification
-   Notice period detection
-   Contract comparison

### Contract Risk Assessment

LegalLens also provides an **indicative contract risk assessment** based
on predefined NLP rules.

The system identifies potentially unfavorable contractual conditions
such as:

-   Automatic renewal
-   Long notice periods
-   Termination penalties
-   Unlimited liability
-   Broad indemnity clauses
-   Non-compete clauses
-   One-sided termination
-   Unilateral modification
-   Late payment penalties

The detected factors contribute to an overall risk score from **0 to
100**.

      Score Risk Level
  --------- ------------
      0--30 Low
     31--60 Medium
    61--100 High

The system also provides recommendations based on the detected risk
factors.

> **Disclaimer:** The risk assessment is an indicative, project-defined
> NLP-based heuristic and does not constitute legal advice or determine
> whether a contract is legally safe.

------------------------------------------------------------------------

## Technology Stack

-   **Python**
-   **Flask**
-   **spaCy**
-   **Stanza**
-   **Natural Language Processing**
-   **Jinja2**
-   **HTML5**
-   **CSS3**
-   **PDF text extraction**

------------------------------------------------------------------------

## NLP Models

### English

The project uses:

``` text
spaCy 3.8.16
en_core_web_sm 3.8.0
```

### Hindi

Hindi linguistic analysis is performed using:

``` text
Stanza
```

with tokenization, POS tagging, and lemmatization.

------------------------------------------------------------------------

## Project Structure

``` text
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

------------------------------------------------------------------------

## How It Works

The general processing pipeline is:

``` text
Contract Input
      │
      ▼
Text / PDF Extraction
      │
      ▼
Language Selection
   ┌──┴──┐
English  Hindi
   │      │
   ▼      ▼
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
Summary / Simplification / Report
```

------------------------------------------------------------------------

## Installation

### 1. Clone the repository

``` bash
git clone <your-github-repository-url>
```

### 2. Navigate to the project

``` bash
cd Intelligent-Legal-Contract-Analyzer
```

### 3. Create a virtual environment

``` bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows

``` powershell
.venv\Scripts\activate
```

### 5. Install dependencies

``` bash
pip install -r requirements.txt
```

### 6. Install the English spaCy model

``` bash
python -m spacy download en_core_web_sm
```

------------------------------------------------------------------------

## Running the Application

Start the Flask application:

``` bash
python app.py
```

The application will be available at:

``` text
http://127.0.0.1:5000
```

Open the address in a web browser.

------------------------------------------------------------------------

## Example Risk Assessment

For example, a contract containing:

``` text
The agreement shall automatically renew.
The employee shall be liable for all losses.
```

may produce:

``` text
Risk Score: 35 / 100
Risk Level: Medium

Detected Factors:
- Automatic Renewal
- Unlimited Liability
```

The system then provides recommendations for reviewing the identified
contractual conditions.

------------------------------------------------------------------------

## Limitations

-   Risk assessment is rule-based and indicative.
-   The system does not provide legal advice.
-   Detection depends on the wording present in the contract.
-   The current implementation is intended primarily for academic and
    educational purposes.
-   Complex legal interpretations may require review by a qualified
    legal professional.

------------------------------------------------------------------------

## Project Purpose

LegalLens is developed as an academic NLP project to demonstrate how
Natural Language Processing techniques can be applied to legal documents
for information extraction, linguistic analysis, contract understanding,
and preliminary risk identification.

------------------------------------------------------------------------

## Disclaimer

LegalLens is an academic/project implementation intended for educational
and research purposes.

The information generated by the system should not be considered
professional legal advice. Users should consult a qualified legal
professional for legal interpretation or contractual decisions.
