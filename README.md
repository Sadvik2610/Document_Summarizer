
# Document Summarizer

A web application for automatic document summarization, powered by FastAPI and Google Generative AI. This application extracts text from various document formats (PDF, DOCX, plain text, and images) and provides concise summaries in simple terms.

---

## Features

- Supports PDF, DOCX, TXT, and image-based documents.
- Uses Google Generative AI (Gemini-1.5-flash model) for intelligent summarization.
- Simple and user-friendly web interface.
- Extensible with FastAPI for additional features.

---

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Google Generative AI API access (API key required)

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/document-summarizer.git
   cd document-summarizer
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Google API Key**:
   Replace `GOOGLE_API_KEY` in `main.py` with your actual Google Generative AI API key.

---

## Usage

1. **Run the Application**:

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:8000/`.

3. **Upload a File**:

   - Click on the "Choose File" button and upload a document (.pdf, .docx, .txt, or image).
   - Click on "Summarize" to get a concise summary of the document.

---

## Project Structure

```
.
|-- main.py                 # FastAPI backend logic
|-- templates/              # HTML templates
|   |-- index.html          # Main page template
|   |-- result.html         # Result page template
|-- static/                 # CSS and static files
|-- requirements.txt        # Project dependencies
```

---

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **python-multipart**: For handling file uploads
- **python-docx**: For extracting text from DOCX files
- **PyPDF2**: For extracting text from PDF files
- **google.generativeai**: For summarization using Google Generative AI
- **Pillow**: For handling image-based files
- **jinja2**: For HTML templating

---

