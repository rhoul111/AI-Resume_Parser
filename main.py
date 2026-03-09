from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import pdfplumber
import io
import os
import json

app = FastAPI(
    title="AI Resume Parser API",
    description="Extracts structured data from resumes — name, contact info, skills, experience, and education.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Input/Output schemas ───────────────────────────────────────────────────────

class TextInput(BaseModel):
    text: str  # raw resume text


class ParsedResume(BaseModel):
    name: str | None
    email: str | None
    phone: str | None
    location: str | None
    linkedin: str | None
    summary: str | None
    skills: list[str]
    experience: list[dict]   # [{title, company, dates, description}]
    education: list[dict]    # [{degree, institution, dates, gpa}]
    certifications: list[str]
    languages: list[str]


# ── Claude parsing logic ───────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precise resume parser. 
Given resume text, extract all information and return ONLY a valid JSON object.
No markdown, no backticks, no extra text — raw JSON only.

JSON shape:
{
  "name": string or null,
  "email": string or null,
  "phone": string or null,
  "location": string or null,
  "linkedin": string or null,
  "summary": string or null,
  "skills": [list of strings],
  "experience": [
    {
      "title": string,
      "company": string,
      "dates": string,
      "description": string
    }
  ],
  "education": [
    {
      "degree": string,
      "institution": string,
      "dates": string,
      "gpa": string or null
    }
  ],
  "certifications": [list of strings],
  "languages": [list of strings]
}

If a field has no data, use null or an empty list as appropriate.
"""

def parse_with_claude(resume_text: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Parse this resume:\n\n{resume_text}"}
        ]
    )

    raw = message.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse resume — Claude returned invalid JSON.")


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Resume Parser API is running."}


@app.post("/parse/text", response_model=ParsedResume, summary="Parse resume from raw text")
def parse_text(body: TextInput):
    """
    Send raw resume text, get back structured JSON.
    """
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    return parse_with_claude(body.text)


@app.post("/parse/pdf", response_model=ParsedResume, summary="Parse resume from PDF upload")
async def parse_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF resume, get back structured JSON.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()

    try:
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read PDF. Make sure it's a valid, text-based PDF.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF appears to be empty or image-only (no extractable text).")

    return parse_with_claude(text)
