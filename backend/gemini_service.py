import os
import time
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the free-tier model
# MODEL_NAME = "gemini-1.5-flash"
# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-2.0-flash-lite"

SYSTEM_PROMPT = """You are an experienced technical interviewer conducting a face-to-face IT job interview.

Rules you MUST follow:
- Keep your responses SHORT and conversational (2-4 sentences max), just like a real interviewer would speak.
- Ask ONE question at a time. Never ask multiple questions together.
- React naturally to the candidate's answer before asking the next question (e.g., "Good point." / "Interesting approach." / "I see.").
- If an answer is vague or incomplete, probe deeper with a follow-up question instead of moving on.
- Cover topics relevant to the role: data structures, algorithms, system design, OOP, databases, problem-solving, and behavioral questions.
- After 8-10 exchanges, wrap up the interview naturally and give brief feedback.
- Never break character. Never say you are an AI.
- Speak in plain, clear English — no markdown, no bullet points, no code blocks (you are speaking out loud).
"""


# async def get_opening_question(role: str, level: str) -> str:
#     """Generate the interviewer's opening line + first question."""
#     model = genai.GenerativeModel(
#         model_name=MODEL_NAME,
#         system_instruction=SYSTEM_PROMPT,
#     )

#     prompt = (
#         f"Start the interview for a {level}-level {role} position. "
#         f"Greet the candidate warmly in 1 sentence, then ask your first question."
#     )

#     response = model.generate_content(prompt)
#     return response.text.strip()


# async def get_interview_response(user_answer: str, history: list) -> str:
#     """
#     Given the candidate's latest answer and the full conversation history,
#     return the interviewer's next response/question.

#     history format: [{"role": "interviewer" | "candidate", "text": "..."}]
#     """
#     model = genai.GenerativeModel(
#         model_name=MODEL_NAME,
#         system_instruction=SYSTEM_PROMPT,
#     )

#     # Build the conversation context string
#     context_lines = []
#     for entry in history:
#         speaker = "Interviewer" if entry["role"] == "interviewer" else "Candidate"
#         context_lines.append(f"{speaker}: {entry['text']}")

#     context = "\n".join(context_lines)

#     prompt = (
#         f"Conversation so far:\n{context}\n\n"
#         f"Candidate just said: \"{user_answer}\"\n\n"
#         f"Respond as the interviewer."
#     )

#     response = model.generate_content(prompt)
#     return response.text.strip()

## working
# async def get_opening_question(role: str, level: str) -> str:
#     print(f"[GEMINI] Generating opening question for {level} {role}")
#     model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
#     prompt = f"Start the interview for a {level}-level {role} position. Greet the candidate warmly in 1 sentence, then ask your first question."
#     response = model.generate_content(prompt)
#     print(f"[GEMINI] Response: {response.text.strip()[:80]}...")
#     return response.text.strip()

# async def get_interview_response(user_answer: str, history: list) -> str:
#     print(f"[GEMINI] User answer received: {user_answer[:80]}...")
#     model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
#     context_lines = []
#     for entry in history:
#         speaker = "Interviewer" if entry["role"] == "interviewer" else "Candidate"
#         context_lines.append(f"{speaker}: {entry['text']}")
#     context = "\n".join(context_lines)
#     prompt = f"Conversation so far:\n{context}\n\nCandidate just said: \"{user_answer}\"\n\nRespond as the interviewer."
#     response = model.generate_content(prompt)
#     print(f"[GEMINI] Interviewer response: {response.text.strip()[:80]}...")
#     return response.text.strip()



# async def get_opening_question(role: str, level: str) -> str:
#     print(f"[GEMINI] Generating opening question for {level} {role}")
#     model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
#     prompt = f"Start the interview for a {level}-level {role} position. Greet the candidate warmly in 1 sentence, then ask your first question."
#     for attempt in range(3):
#         try:
#             response = model.generate_content(prompt)
#             print(f"[GEMINI] Response: {response.text.strip()[:80]}...")
#             return response.text.strip()
#         except Exception as e:
#             print(f"[GEMINI] Attempt {attempt+1} failed: {e}")
#             if attempt < 2:
#                 time.sleep(20)
#     return "Hello! Let's begin. Can you tell me about yourself?"

# async def get_interview_response(user_answer: str, history: list) -> str:
#     print(f"[GEMINI] User answer received: {user_answer[:80]}...")
#     model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_PROMPT)
#     context_lines = []
#     for entry in history:
#         speaker = "Interviewer" if entry["role"] == "interviewer" else "Candidate"
#         context_lines.append(f"{speaker}: {entry['text']}")
#     context = "\n".join(context_lines)
#     prompt = f"Conversation so far:\n{context}\n\nCandidate just said: \"{user_answer}\"\n\nRespond as the interviewer."
#     for attempt in range(3):
#         try:
#             response = model.generate_content(prompt)
#             print(f"[GEMINI] Interviewer response: {response.text.strip()[:80]}...")
#             return response.text.strip()
#         except Exception as e:
#             print(f"[GEMINI] Attempt {attempt+1} failed: {e}")
#             if attempt < 2:
#                 time.sleep(20)
#     return "Interesting. Could you elaborate a bit more on that?"


MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
]

async def _generate(prompt: str) -> str:
    for model_name in MODELS_TO_TRY:
        try:
            print(f"[GEMINI] Trying model: {model_name}")
            model = genai.GenerativeModel(model_name=model_name, system_instruction=SYSTEM_PROMPT)
            response = model.generate_content(prompt)
            print(f"[GEMINI] Success with {model_name}")
            return response.text.strip()
        except Exception as e:
            print(f"[GEMINI] {model_name} failed: {str(e)[:80]}")
            continue
    return "Could you elaborate more on your previous answer?"

async def get_opening_question(role: str, level: str) -> str:
    prompt = f"Start the interview for a {level}-level {role} position. Greet the candidate warmly in 1 sentence, then ask your first question."
    return await _generate(prompt)

async def get_interview_response(user_answer: str, history: list) -> str:
    context = "\n".join(f"{'Interviewer' if e['role']=='interviewer' else 'Candidate'}: {e['text']}" for e in history)
    prompt = f"Conversation so far:\n{context}\n\nCandidate just said: \"{user_answer}\"\n\nRespond as the interviewer."
    return await _generate(prompt)