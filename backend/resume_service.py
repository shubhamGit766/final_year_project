import os
import json
import re
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Try cheaper/higher-quota models first, gemini-2.5-flash last (strictest free tier: 5 RPM)
MODELS_TO_TRY = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-2.5-flash",
]


def extract_text_from_pdf(file_path: str) -> str:
    import fitz
    print(f"[RESUME] Extracting text from PDF: {file_path}")
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    print(f"[RESUME] Extracted {len(text)} characters from PDF")
    return text.strip()


async def analyze_resume(resume_text: str, job_role: str) -> dict:
    print(f"[RESUME] Analyzing resume for role: {job_role}")

    key = os.getenv("GEMINI_RESUME_KEY")
    if not key:
        raise ValueError("GEMINI_RESUME_KEY is missing from your .env file")

    print(f"[RESUME] Using key: {key[:10]}...")
    genai.configure(api_key=key)

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and resume reviewer.

Analyze the following resume for a {job_role} position and respond ONLY with a valid JSON object (no markdown, no backticks, no explanation).

Resume:
{resume_text}

Return this exact JSON structure:
{{
  "ats_score": <integer 0-100>,
  "score_breakdown": {{
    "keywords": <integer 0-25>,
    "formatting": <integer 0-25>,
    "experience": <integer 0-25>,
    "skills": <integer 0-25>
  }},
  "missing_keywords": [<list of 5-8 important missing keywords for {job_role}>],
  "strengths": [<list of 3 strengths found in the resume>],
  "improvements": [<list of 3-4 specific improvement suggestions>],
  "youtube_queries": [<list of 4 specific YouTube search queries to help improve weak areas>],
  "candidate_name": "<name from resume or 'Candidate'>",
  "detected_role": "<current role/title detected from resume>"
}}
"""

    last_error = None

    for model_name in MODELS_TO_TRY:
        try:
            print(f"[RESUME] Trying model: {model_name}")
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            raw = response.text.strip()
            print(f"[RESUME] Success with {model_name}. Raw: {raw[:120]}...")
            raw = re.sub(r"```json|```", "", raw).strip()
            result = json.loads(raw)
            print(f"[RESUME] ATS Score: {result.get('ats_score')}")
            return result
        except Exception as e:
            print(f"[RESUME] {model_name} failed: {str(e)[:120]}")
            last_error = e
            continue

    raise Exception(f"All Gemini models failed for resume analysis. Last error: {last_error}")