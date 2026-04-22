import os
import time
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env file
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Configuration Constants
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.5-flash"

# Lazy Client Initialization
_groq_client = None
_gemini_configured = False

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            # Raising a clearer error helps debugging
            raise ValueError("GROQ_API_KEY is missing from your environment/ .env file")
        _groq_client = Groq(api_key=key)
    return _groq_client

def configure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        key = os.getenv("GEMINI_INTERVIEW_KEY")
        if not key:
            raise ValueError("GEMINI_INTERVIEW_KEY is missing from your environment/ .env file")
        genai.configure(api_key=key)
        _gemini_configured = True

def build_system_prompt(role: str, level: str, resume_text: str = "") -> str:
    resume_section = ""
    if resume_text:
        resume_section = f"""
The candidate's resume is provided below. Use it to ask personalized questions about their actual experience, projects, and skills. Reference specific things from their resume naturally, like a real interviewer would.

RESUME:
{resume_text[:3000]}
"""
    return f"""You are an experienced technical interviewer conducting a face-to-face IT job interview for a {level}-level {role} position.
{resume_section}
Rules you MUST follow:
- Keep your responses SHORT and conversational (2-4 sentences max), just like a real interviewer would speak.
- Ask ONE question at a time. Never ask multiple questions together.
- React naturally to the candidate's answer before asking the next question (e.g., "Good point." / "Interesting." / "I see.").
- If an answer is vague or incomplete, probe deeper with a follow-up question.
- Mix technical and behavioral questions. Reference the resume when relevant.
- After 8-10 exchanges, wrap up naturally and give brief honest feedback.
- Never break character. Never say you are an AI.
- Speak in plain, clear English — no markdown, no bullet points, no code blocks.
"""

async def _try_groq(messages: list) -> str:
    print("[GROQ] Sending request...")
    client = get_groq_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=200,
    )
    result = response.choices[0].message.content.strip()
    print(f"[GROQ] Response: {result[:80]}...")
    return result

async def _try_gemini(system_prompt: str, messages: list) -> str:
    print("[GEMINI] Falling back to Gemini...")
    configure_gemini()
    model = genai.GenerativeModel(model_name=GEMINI_MODEL, system_instruction=system_prompt)
    
    # Convert message history to a single string for Gemini
    convo = "\n".join(
        f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {m['content']}"
        for m in messages if m["role"] != "system"
    )
    
    response = model.generate_content(convo + "\n\nRespond as the interviewer.")
    result = response.text.strip()
    print(f"[GEMINI] Response: {result[:80]}...")
    return result

async def get_opening_question(role: str, level: str, resume_text: str = "") -> str:
    system_prompt = build_system_prompt(role, level, resume_text)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Start the interview. Greet the candidate warmly in 1 sentence, then ask your first question based on their resume and the {level}-level {role} role."}
    ]
    try:
        return await _try_groq(messages)
    except Exception as e:
        print(f"[GROQ] Failed: {str(e)[:80]}")
        try:
            return await _try_gemini(system_prompt, messages)
        except Exception as e2:
            print(f"[GEMINI] Failed: {str(e2)[:80]}")
            return "Welcome! Thanks for joining us today. Could you start by walking me through your background and what you've been working on recently?"

async def get_interview_response(user_answer: str, history: list, role: str = "Software Engineer", level: str = "Mid", resume_text: str = "") -> str:
    system_prompt = build_system_prompt(role, level, resume_text)

    messages = [{"role": "system", "content": system_prompt}]
    for entry in history:
        role_key = "assistant" if entry["role"] == "interviewer" else "user"
        messages.append({"role": role_key, "content": entry["text"]})
    messages.append({"role": "user", "content": user_answer})

    try:
        return await _try_groq(messages)
    except Exception as e:
        print(f"[GROQ] Failed: {str(e)[:80]}")
        try:
            return await _try_gemini(system_prompt, messages)
        except Exception as e2:
            print(f"[GEMINI] Failed: {str(e2)[:80]}")
            return "Interesting point. Could you elaborate a bit more on that?"