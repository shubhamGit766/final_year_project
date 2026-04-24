import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Models to try in order (all free on Groq)
MODELS_TO_TRY = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

_client = None

def get_client():
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY is missing from environment")
        _client = Groq(api_key=key)
    return _client


def extract_text_from_pdf(file_path: str) -> str:
    import fitz
    print(f"[RESUME] Extracting text from PDF: {file_path}")
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    print(f"[RESUME] Extracted {len(text)} characters")
    return text.strip()


async def analyze_resume(resume_text: str, job_role: str) -> dict:
    print(f"[RESUME] Analyzing resume for role: {job_role}")

    prompt = f"""You are an expert ATS (Applicant Tracking System) and resume reviewer.

Analyze the following resume for a {job_role} position.
Respond ONLY with a valid JSON object. No markdown, no backticks, no explanation, no text before or after the JSON.

Resume:
{resume_text[:4000]}

Return EXACTLY this JSON structure:
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
}}"""

    client = get_client()
    last_error = None

    for model in MODELS_TO_TRY:
        try:
            print(f"[RESUME] Trying Groq model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.3,
            )
            raw = response.choices[0].message.content.strip()
            print(f"[RESUME] Got response from {model}: {raw[:100]}...")

            # Strip any accidental markdown fences
            raw = re.sub(r"```json|```", "", raw).strip()

            # Find JSON object in response
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                raw = match.group()

            result = json.loads(raw)
            print(f"[RESUME] ATS Score: {result.get('ats_score')}")
            return result

        except json.JSONDecodeError as e:
            print(f"[RESUME] JSON parse error with {model}: {e}")
            last_error = e
            continue
        except Exception as e:
            print(f"[RESUME] {model} failed: {str(e)[:100]}")
            last_error = e
            continue

    raise Exception(f"All Groq models failed for resume analysis. Last error: {last_error}")