from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

print("🚀 App starting...")

# Get current working directory
BASE_DIR = os.getcwd()
print(f"📁 BASE_DIR: {BASE_DIR}")

# Debug: list files
try:
    files = os.listdir(BASE_DIR)
    print(f"📂 Files in BASE_DIR: {files}")
except Exception as e:
    print(f"❌ Error reading directory: {e}")

# Try mounting static only if exists
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    print(f"✅ Static folder found: {STATIC_DIR}")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"⚠️ Static folder NOT found at: {STATIC_DIR}")

# Root route
@app.get("/")
def read_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    print(f"📄 Looking for index.html at: {index_path}")

    if os.path.exists(index_path):
        print("✅ index.html found")
        return FileResponse(index_path)
    else:
        print("❌ index.html NOT found")
        return JSONResponse(
            status_code=404,
            content={"error": "index.html not found"}
        )

# Health check (very important for Railway)
@app.get("/health")
def health():
    return {"status": "ok"}

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