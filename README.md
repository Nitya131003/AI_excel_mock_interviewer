# AI Excel Interviewer

A web application built with **FastAPI** that conducts mock Excel technical interviews by randomly selecting questions, evaluating candidate answers using Azure OpenAI GPT, and generating a downloadable PDF summary report.

---

## ✅ Features

- Randomly selects 5 questions per interview from a larger question pool.
- Evaluates candidate’s answers using Azure OpenAI GPT API.
- Provides a score (0–10) and short constructive feedback.
- Saves all questions, answers, scores, and feedback in an SQLite database.
- Displays a summary report after the interview.
- Allows downloading the summary report as a PDF.

---

## ✅ Tech Stack

- Backend: FastAPI
- Database: SQLite
- Template Engine: Jinja2
- External API: Azure OpenAI GPT
- PDF Generation: ReportLab
- Deployment Target: Render.com

---

## ✅ Setup Instructions

### 1. Clone the project
```bash
git clone https://github.com/your-username/ai_excel_mock_interviewer.git
cd ai_excel_mock_interviewer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add environment variables
Create a ```.env``` file with

### 4. Run locally
```bash
uvicorn main:app --reload
```
Visit:
```bash
http://127.0.0.1:8000
```

---

# ✅ Usage

1. Visit homepage.  
2. Answer 5 randomly selected Excel technical questions.  
3. After the interview, view the summary report.  
4. Download the summary as a PDF.  

---
