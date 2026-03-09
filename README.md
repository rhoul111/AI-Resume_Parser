# Resume Parser API

An AI-powered REST API that extracts structured data from resumes. Send a PDF or plain text resume, receive a clean JSON object — no templates, no regex, no brittle rules.

Built with [FastAPI](https://fastapi.tiangolo.com/) and [Claude](https://anthropic.com) (Anthropic).

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/parse/text` | Parse resume from raw text |
| `POST` | `/parse/pdf` | Parse resume from PDF upload |

Full interactive docs available at `/docs` when running locally.

---

## Response Schema

Both endpoints return the same JSON structure:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1 415 555 0192",
  "location": "San Francisco, CA",
  "linkedin": "linkedin.com/in/janedoe",
  "summary": "Senior PM with 6 years experience...",
  "skills": ["Python", "SQL", "Figma"],
  "experience": [
    {
      "title": "Senior Product Manager",
      "company": "Stripe",
      "dates": "Jan 2021 – Present",
      "description": "Led payments infrastructure team..."
    }
  ],
  "education": [
    {
      "degree": "B.S. Computer Science",
      "institution": "MIT",
      "dates": "2018",
      "gpa": "3.8"
    }
  ],
  "certifications": ["AWS Certified Solutions Architect"],
  "languages": ["English", "French"]
}
```

Fields with no data return `null` or an empty list `[]`.

---

## Running Locally

### Prerequisites
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/resume-parser-api.git
cd resume-parser-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 4. Start the server
uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`.
Visit `http://localhost:8000/docs` for the auto-generated interactive docs.

---

## Example Requests

### Parse from text

```bash
curl -X POST "http://localhost:8000/parse/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jane Doe\njane@email.com\n\nExperience:\nProduct Manager at Stripe, 2021-Present..."}'
```

### Parse from PDF

```bash
curl -X POST "http://localhost:8000/parse/pdf" \
  -F "file=@resume.pdf"
```

---

## Deployment (Railway)

This repo is configured for one-click deployment to [Railway](https://railway.app).

1. Fork this repo
2. Create a new project on Railway → **Deploy from GitHub repo**
3. Select this repo
4. Go to **Variables** and add: `ANTHROPIC_API_KEY=your-key-here`
5. Railway deploys automatically — your live URL appears under **Settings → Domains**

The `railway.toml` and `Procfile` are already configured.

---

## Tech Stack

- **Framework:** FastAPI
- **AI Model:** Claude (Anthropic) via `anthropic` Python SDK
- **PDF Extraction:** pdfplumber
- **Hosting:** Railway

---

## Available on RapidAPI

This API is listed on RapidAPI with a free tier and paid plans.
[→ View on RapidAPI](#) *(link coming soon)*

---

## License

All rights reserved. This code is publicly visible but may not be copied, modified, or redistributed without permission.
