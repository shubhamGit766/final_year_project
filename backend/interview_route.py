from fastapi import APIRouter, UploadFile, File, Form
from interview_controller import start_interview, submit_answer

router = APIRouter()

@router.post("/start")
async def start(
    role: str = Form("Software Engineer"),
    level: str = Form("Mid"),
    resume_text: str = Form("")
):
    return await start_interview(role, level, resume_text)

@router.post("/answer")
async def answer(
    audio: UploadFile = File(...),
    conversation_history: str = Form(...),
    role: str = Form("Software Engineer"),
    level: str = Form("Mid"),
    resume_text: str = Form("")
):
    return await submit_answer(audio, conversation_history, role, level, resume_text)