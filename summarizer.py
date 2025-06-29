from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai

GOOGLE_API_KEY = "YOUR_GEMINI_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory document storage (for simplicity)
doc_store = {}

def extract_text_from_pdf(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    return "\n".join([p.text for p in doc.paragraphs])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize")
async def summarize(request: Request, file: UploadFile = File(...)):
    file_type = file.content_type
    file_data = await file.read()

    # Extract text
    if file_type == "application/pdf":
        text = extract_text_from_pdf(file_data)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(file_data)
    elif file_type.startswith("text/"):
        text = file_data.decode("utf-8")
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    if not text.strip():
        return JSONResponse(content={"error": "No readable text found"}, status_code=400)

    summary = model.generate_content([
        text,
        "summarize this document and explain in simple terms with side headings. do not use bold font."
    ])

    # Store for session use
    doc_store["text"] = text

    return templates.TemplateResponse("result.html", {
        "request": request,
        "summary": summary.text
    })

@app.post("/qa")
async def ask_anything(request: Request, question: str = Form(...)):
    text = doc_store.get("text")
    if not text:
        return JSONResponse(content={"error": "Document not loaded"}, status_code=400)

    response = model.generate_content([
        text,
        f"Answer the following question based on the document:\n{question}"
    ])

    return templates.TemplateResponse("qa.html", {
        "request": request,
        "question": question,
        "answer": response.text
    })

@app.get("/challenge")
async def challenge_me(request: Request):
    text = doc_store.get("text")
    if not text:
        return JSONResponse(content={"error": "Document not loaded"}, status_code=400)

    response = model.generate_content([
        text,
        "Generate 3 logic-based or comprehension-focused questions based on this document. Number them 1 to 3."
    ])

    doc_store["challenge_questions"] = response.text

    return templates.TemplateResponse("challenge.html", {
        "request": request,
        "questions": response.text
    })

@app.post("/evaluate")
async def evaluate_answers(
    request: Request,
    answer1: str = Form(...),
    answer2: str = Form(...),
    answer3: str = Form(...)
):
    text = doc_store.get("text")
    questions = doc_store.get("challenge_questions")
    if not (text and questions):
        return JSONResponse(content={"error": "Challenge session not initialized"}, status_code=400)

    user_answers = f"Q1: {answer1}\nQ2: {answer2}\nQ3: {answer3}"

    eval_prompt = (
        f"Document:\n{text}\n\n"
        f"Questions:\n{questions}\n\n"
        f"User's Answers:\n{user_answers}\n\n"
        f"Evaluate the user's answers based on the document. For each question, give feedback and explain based on the document."
    )

    response = model.generate_content(eval_prompt)

    return templates.TemplateResponse("evaluation.html", {
        "request": request,
        "feedback": response.text
    })
