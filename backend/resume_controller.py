import os
import tempfile
from datetime import datetime
from fastapi import UploadFile
from resume_service import extract_text_from_pdf, analyze_resume
from database import resumes_collection


async def analyze_resume_controller(file: UploadFile, job_role: str, user_id: str = None) -> dict:
    print(f"\n[CONTROLLER] Resume upload received for role: {job_role}, user: {user_id}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        resume_text = extract_text_from_pdf(tmp_path)

        if not resume_text or len(resume_text) < 50:
            return {"error": "Could not extract text from PDF. Please ensure it is not scanned/image-based."}

        result = await analyze_resume(resume_text, job_role)

        # Generate YouTube links
        yt_links = []
        for query in result.get("youtube_queries", []):
            encoded = query.replace(" ", "+")
            yt_links.append({"label": query, "url": f"https://www.youtube.com/results?search_query={encoded}"})
        result["youtube_links"] = yt_links
        result["resume_text"] = resume_text
        result["job_role"] = job_role

        # Save to MongoDB if user is logged in
        if user_id:
            resume_doc = {
                "user_id": user_id,
                "job_role": job_role,
                "candidate_name": result.get("candidate_name", ""),
                "detected_role": result.get("detected_role", ""),
                "ats_score": result.get("ats_score"),
                "score_breakdown": result.get("score_breakdown"),
                "missing_keywords": result.get("missing_keywords", []),
                "strengths": result.get("strengths", []),
                "improvements": result.get("improvements", []),
                "analyzed_at": datetime.utcnow(),
            }
            await resumes_collection.insert_one(resume_doc)
            print(f"[CONTROLLER] Resume saved to MongoDB for user: {user_id}")

        print(f"[CONTROLLER] Analysis complete. Score: {result.get('ats_score')}")
        return result

    finally:
        os.unlink(tmp_path)


async def get_resume_history(user_id: str) -> list:
    """Fetch all past resume analyses for a user."""
    cursor = resumes_collection.find(
        {"user_id": user_id},
        {"_id": 0}  # exclude mongo _id from response
    ).sort("analyzed_at", -1)  # newest first

    history = []
    async for doc in cursor:
        doc["analyzed_at"] = doc["analyzed_at"].isoformat()
        history.append(doc)

    return history

# import os
# import tempfile
# from fastapi import UploadFile
# from resume_service import extract_text_from_pdf, analyze_resume


# async def analyze_resume_controller(file: UploadFile, job_role: str) -> dict:
#     print(f"\n[CONTROLLER] Resume upload received for role: {job_role}")

#     # Save uploaded PDF to temp file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(await file.read())
#         tmp_path = tmp.name

#     try:
#         # Extract text
#         resume_text = extract_text_from_pdf(tmp_path)

#         if not resume_text or len(resume_text) < 50:
#             return {"error": "Could not extract text from PDF. Please ensure it is not scanned/image-based."}

#         # Analyze with Gemini
#         result = await analyze_resume(resume_text, job_role)

#         # Generate YouTube links from queries
#         yt_links = []
#         for query in result.get("youtube_queries", []):
#             encoded = query.replace(" ", "+")
#             yt_links.append({
#                 "label": query,
#                 "url": f"https://www.youtube.com/results?search_query={encoded}"
#             })
#         result["youtube_links"] = yt_links

#         # Store resume text in result so interview can use it
#         result["resume_text"] = resume_text
#         result["job_role"] = job_role

#         print(f"[CONTROLLER] Analysis complete. Score: {result.get('ats_score')}")
#         return result

#     finally:
#         os.unlink(tmp_path)
