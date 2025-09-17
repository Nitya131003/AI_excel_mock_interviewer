from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
import sqlite3
import os
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

AZURE_API_URL = f"{AZURE_API_BASE}/openai/deployments/{MODEL_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_API_VERSION}"

headers = {
    "api-key": AZURE_API_KEY,
    "Content-Type": "application/json"
}


# Initialize DB
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        score INTEGER,
        feedback TEXT
    )
''')
conn.commit()


# Sample Questions
QUESTIONS = [
    "How do you use VLOOKUP in Excel?",
    "Explain pivot tables and how you would use them.",
    "What is conditional formatting in Excel and provide an example use-case?",
    "How do you protect cells in an Excel worksheet?",
    "What is the difference between relative and absolute cell references in Excel?",
    "How do you use the IF function in Excel?",
    "What are named ranges and why are they useful?",
    "Explain data validation in Excel with an example.",
    "How do you create a chart in Excel?",
    "What is the purpose of the CONCATENATE function in Excel?"
]

import random

selected_questions = [] 


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    global selected_questions
    selected_questions = random.sample(QUESTIONS, 5)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM interviews')
    conn.commit()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "question": selected_questions[0], "index": 0})


@app.post("/interview", response_class=HTMLResponse)
async def interview(request: Request, answer: str = Form(...), index: int = Form(...)):
    question = selected_questions[index]
    
    prompt = f"""
    You are an expert Excel interviewer. Evaluate the following candidate's response in terms of correctness, depth, and clarity.

    Provide:
    1. A score from 0 to 10.
    2. A concise feedback of no more than 3 sentences.

    Response format:
    Score: <score out of 10>
    Feedback: <short constructive feedback (max 3 sentences)>
    
    Question: {question}
    Candidate's Answer: {answer}
    """

    data = {
        "messages": [
            {"role": "system", "content": "You are an Excel interview expert."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }


    response = requests.post(AZURE_API_URL, headers=headers, json=data)
    response_json = response.json()

    print("Azure API Response:", response_json)

    try:
        result = response_json['choices'][0]['message']['content']
    except (KeyError, IndexError):
        result = "Error: Unable to get evaluation from API."
        print("Full API Response:", response_json)
    
    import re

    score_match = re.search(r"\*{0,2}Score\*{0,2}\s*:\s*(\d+)", result, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0

    feedback_match = re.search(r"\*{0,2}Feedback\*{0,2}\s*:\s*(.*)", result, re.IGNORECASE | re.DOTALL)
    if feedback_match:
        feedback = feedback_match.group(1).strip().replace('\n', ' ')
        if len(feedback) > 500:
            feedback = feedback[:500] + '...'
    else:
        feedback = "No feedback available."


    # Save to DB
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO interviews (question, answer, score, feedback) VALUES (?, ?, ?, ?)',
              (question, answer, score, feedback))
    conn.commit()

    next_index = index + 1

    if next_index < len(selected_questions):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "question": selected_questions[next_index],
            "index": next_index
        })
    else:
        # Generate Summary Report
        c.execute('SELECT question, answer, score, feedback FROM interviews')
        records = c.fetchall()
        conn.close()

        if records:
            overall_score = round(sum([r[2] for r in records]) / len(records), 2)
        else:
            overall_score = 0

        return templates.TemplateResponse("summary.html", {
            "request": request,
            "records": records,
            "overall_score": round(overall_score, 2)
        })
        

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from fastapi.responses import FileResponse  

@app.get("/download-pdf-report")
async def download_pdf_report():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT question, answer, score, feedback FROM interviews')
    records = c.fetchall()
    conn.close()

    pdf_filename = "interview_summary_report.pdf"

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Interview Summary Report", styles['Title']))
    overall_score = round(sum([r[2] for r in records]) / len(records), 2) if records else 0
    elements.append(Paragraph(f"Overall Score: {overall_score}/10", styles['Heading2']))
    elements.append(Spacer(1, 20))

    # Table header and data
    data = [[
        Paragraph("<b>Question</b>", styles['Normal']),
        Paragraph("<b>Answer</b>", styles['Normal']),
        Paragraph("<b>Score</b>", styles['Normal']),
        Paragraph("<b>Feedback</b>", styles['Normal'])
    ]]

    for row in records:
        question, answer, score, feedback = row
        data.append([
            Paragraph(question, styles['Normal']),
            Paragraph(answer, styles['Normal']),
            Paragraph(str(score), styles['Normal']),
            Paragraph(feedback, styles['Normal'])
        ])

    table = Table(data, colWidths=[150, 150, 50, 200])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (2,1), (2,-1), 'CENTER')
    ]))

    elements.append(table)

    doc.build(elements)

    return FileResponse(pdf_filename, media_type='application/pdf', filename=pdf_filename)