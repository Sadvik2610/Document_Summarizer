from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyADo6gy_Bv4AqLK5Z8nlckLwHrt8jfxGs8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def extract_text_from_pdf(pdf_bytes):
    reader = PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_bytes):
    doc = Document(BytesIO(docx_bytes))
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

@app.post("/summarize")
async def summarize(request: Request, file: UploadFile = File(...)):
    file_type = file.content_type
    file_data = await file.read()

    if file_type == "application/pdf":
        text = extract_text_from_pdf(file_data)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(file_data)
    elif file_type.startswith("text/"):
        text = file_data.decode("utf-8")
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)
    summary = model.generate_content([text, "summarize this document and explain in simple terms with side headings."])
    
    return templates.TemplateResponse("result.html", {"request": request, "summary": summary.text})