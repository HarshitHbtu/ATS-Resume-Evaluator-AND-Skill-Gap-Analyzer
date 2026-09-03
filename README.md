# 📄 Resume Score Generator

An web application that analyzes a resume against a Job Description and generates an **ATS compatibility score** using NLP and semantic similarity.

## 🚀 Key Features

* 📄 Supports **PDF & DOCX** resumes
* 🧠 Semantic similarity using **Sentence Transformers**
* 🛠️ Resume–JD **skill matching**
* 🎓 Degree requirement matching
* 🔗 GitHub/LinkedIn/Portfolio detection
* 🎯 Final **ATS Score out of 100**
* ❌ Identifies missing skills
* 💡 Provides resume improvement suggestions

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – Web UI
* **Sentence Transformers** – Text embeddings
* **all-MiniLM-L6-v2** – Pre-trained NLP model
* **NumPy** – Score calculation
* **NLP & Cosine Similarity** – Resume-JD matching

## 🏗️ Architecture

```text
Resume (PDF/DOCX)          Job Description
        │                         │
        ▼                         ▼
  Text Extraction          Text Preprocessing
        │                         │
        └──────────┬──────────────┘
                   ▼
          Semantic Similarity
          (Sentence Transformer)
                   │
                   ▼
             Skill Matching
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Degree Matching    Portfolio Check
          │                 │
          └────────┬────────┘
                   ▼
             ATS Score (100)
                   │
                   ▼
       Missing Skills + Suggestions
```

## 📊 Score Breakdown

| Component           |   Score |
| ------------------- | ------: |
| Semantic Similarity |      30 |
| Skill Match         |      50 |
| Degree Match        |      10 |
| Portfolio           |      10 |
| **Total**           | **100** |

## 📁 Project Structure

```text
├── app.py
├── requirements.txt
└── source/
    ├── parser.py
    ├── preprocessing.py
    ├── skill_match.py
    └── ats_score.py
```

## ▶️ Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ⚠️ Disclaimer

The generated score is an **estimated ATS compatibility score** and may differ from the scoring systems used by real companies.
