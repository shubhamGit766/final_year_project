import json
import tempfile
import os
from fastapi import UploadFile
from groq_service import get_interview_response, get_opening_question
from stt_service import transcribe_audio
from tts_service import text_to_speech_base64


async def start_interview(role: str, level: str, resume_text: str = "") -> dict:
    print(f"\n[CONTROLLER] Starting interview: {role} / {level} | Resume: {'yes' if resume_text else 'no'}")
    opening_question = await get_opening_question(role, level, resume_text)
    print("[CONTROLLER] Generating TTS for opening...")
    audio_base64 = await text_to_speech_base64(opening_question)
    print("[CONTROLLER] Done! Sending response to frontend.")
    return {"ai_text": opening_question, "audio_base64": audio_base64}


async def submit_answer(audio: UploadFile, conversation_history: str, role: str = "Software Engineer", level: str = "Mid", resume_text: str = "") -> dict:
    print(f"\n[CONTROLLER] Received audio answer")
    suffix = os.path.splitext(audio.filename or "audio.webm")[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name
    print(f"[CONTROLLER] Audio saved to: {tmp_path}")
    try:
        user_text = await transcribe_audio(tmp_path)
        history = json.loads(conversation_history)
        ai_response = await get_interview_response(user_text, history, role, level, resume_text)
        print("[CONTROLLER] Generating TTS for response...")
        audio_base64 = await text_to_speech_base64(ai_response)
        print("[CONTROLLER] Done! Sending response to frontend.")
    finally:
        os.unlink(tmp_path)
    return {"user_text": user_text, "ai_text": ai_response, "audio_base64": audio_base64}