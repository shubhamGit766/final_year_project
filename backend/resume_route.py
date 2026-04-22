from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from resume_controller import analyze_resume_controller, get_resume_history
from dependencies import get_current_user

router = APIRouter()


@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_role: str = Form("Software Engineer"),
    authorization: Optional[str] = None,  # optional — works without login too
):
    user_id = None
    if authorization:
        try:
            from auth_service import decode_access_token
            token = authorization.replace("Bearer ", "")
            payload = decode_access_token(token)
            if payload:
                user_id = payload["sub"]
        except Exception:
            pass

    return await analyze_resume_controller(file, job_role, user_id)


@router.get("/history")
async def history(current_user: dict = Depends(get_current_user)):
    """Returns all past resume analyses for the logged-in user."""
    return await get_resume_history(current_user["user_id"])

# from fastapi import APIRouter, UploadFile, File, Form
# from resume_controller import analyze_resume_controller

# router = APIRouter()

# @router.post("/analyze")
# async def analyze(
#     file: UploadFile = File(...),
#     job_role: str = Form("Software Engineer")
# ):
#     return await analyze_resume_controller(file, job_role)
