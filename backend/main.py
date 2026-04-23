import os
import sys
from pathlib import Path

# Fix imports: add backend/ folder to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from interview_route import router as interview_router
from resume_route import router as resume_router
from auth_route import router as auth_router

app = FastAPI(title="AI Resume & Interview Platform", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])

@app.get("/health")
def health():
    return {"status": "ok"}

ROOT_DIR = Path(__file__).parent.parent

def serve_html(filename: str):
    p = ROOT_DIR / filename
    if p.exists():
        return FileResponse(str(p))
    return JSONResponse({"error": f"{filename} not found"}, status_code=404)

@app.get("/")
def serve_index():
    return serve_html("index.html")

# Handle direct navigation to index.html
@app.get("/index.html")
def serve_index_html():
    return serve_html("index.html")

@app.get("/analysis.html")
def serve_analysis():
    for name in ["analysis.html", "Analysis.html"]:
        p = ROOT_DIR / name
        if p.exists(): return FileResponse(str(p))
    return JSONResponse({"error": "not found"}, status_code=404)

@app.get("/Analysis.html")
def serve_analysis_cap():
    for name in ["Analysis.html", "analysis.html"]:
        p = ROOT_DIR / name
        if p.exists(): return FileResponse(str(p))
    return JSONResponse({"error": "not found"}, status_code=404)

@app.get("/Interview.html")
def serve_interview():
    return serve_html("Interview.html")


# New
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from interview_route import router as interview_router
# from resume_route import router as resume_router
# from auth_route import router as auth_router
# from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# app = FastAPI(title="AI Resume & Interview Platform", version="3.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
# app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
# app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])

# @app.get("/")
# async def root():
#     return {"message": "AI Resume & Interview Platform API is running"}


# #Old
# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from interview_route import router as interview_router
# # from resume_route import router as resume_router
# # from pathlib import Path
# # from dotenv import load_dotenv
# # load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# # app = FastAPI(title="AI Resume & Interview Platform", version="2.0.0")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # app.include_router(interview_router, prefix="/api/interview", tags=["Interview"])
# # app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])

# # @app.get("/")
# # async def root():
# #     return {"message": "AI Resume & Interview Platform API is running"}