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

### 1. Set up Virtual Environment

It is recommended to use a virtual environment to manage dependencies.  

**Command to create a virtual environment:**
```bash
python -m venv venv
```

**Activate the Virtual Environment:**

- **Windows:**
```bash
venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```
### Packages and Their Purpose

This project uses the following Python packages:

- **fastapi** → Web framework to build APIs and handle routes for the interview app.  
- **uvicorn** → ASGI server used to run the FastAPI application.   
- **jinja2** → Template engine to render HTML pages (`index.html`, `summary.html`).  
- **aiofiles** → Handles asynchronous file operations (used internally by FastAPI for static files).  
- **requests** → Makes HTTP requests to Azure OpenAI API for answer evaluation.  
- **python-dotenv** → Loads environment variables (like API keys) from a `.env` file.  
- **reportlab** → Generates PDF reports for interview summaries.  
- **python-multipart** → Enables form data parsing in FastAPI (used when submitting answers).  

### 3. Run locally
```bash
uvicorn main:app --reload
```
Visit:
```bash
http://127.0.0.1:8000
```

---

## Workflow

### 1. Start Interview Session
- User visits the homepage (`/`).
- The app selects **5 random Excel questions** from a predefined list.
- Previous interview data is cleared from the SQLite database.
- The first question is displayed using `index.html`.

### 2. Submit Answer
- Candidate submits an answer through the web form.
- The answer, along with the corresponding question, is sent to the **Azure OpenAI API**.
- The API evaluates the answer and returns:
  - A **score (0–10)**
  - **Constructive feedback (≤3 sentences)**

### 3. Save Data
- Score and feedback, along with the question and answer, are stored in the **SQLite database**.
- If more questions remain:
  - The next question is displayed.
- Otherwise:
  - The **interview summary page** (`summary.html`) is shown.

### 4. Display Summary
- Shows all questions, answers, scores, and feedback.
- Calculates the **overall score** of the candidate.

### 5. Generate PDF Report
- User can click **Download PDF**.
- The app generates a PDF using **ReportLab** with:
  - Interview title
  - Overall score
  - Table of questions, answers, scores, and feedback
- PDF is returned as a downloadable file.

---

## ✅ Usage

1. Visit homepage.  
2. Answer 5 randomly selected Excel technical questions.  
3. After the interview, view the summary report.  
4. Download the summary as a PDF.  

---
