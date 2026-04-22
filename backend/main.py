from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Base directory (backend folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("🚀 App starting...")
print("📁 BASE_DIR:", BASE_DIR)
print("📁 Current Working Dir:", os.getcwd())
print("📂 Files in CWD:", os.listdir("."))

# ✅ Safe static mount
static_path = os.path.join(BASE_DIR, "static")

if os.path.isdir(static_path):
    print("✅ Static folder found:", static_path)
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print("⚠️ Static folder NOT found at:", static_path)

# ✅ Root route (safe + debug)
@app.get("/")
def read_index():
    try:
        print("\n🔍 Incoming request: /")

        # Try multiple possible locations
        possible_paths = [
            os.path.join(BASE_DIR, "index.html"),
            os.path.join(BASE_DIR, "..", "index.html"),
            os.path.join(os.getcwd(), "index.html"),
        ]

        print("📌 Checking index.html in paths:")
        for path in possible_paths:
            print("   ➜", path)

        for path in possible_paths:
            if os.path.exists(path):
                print("✅ Found index.html at:", path)
                return FileResponse(path)

        print("❌ index.html NOT FOUND")
        return JSONResponse(
            content={
                "status": "API running",
                "error": "index.html not found",
                "checked_paths": possible_paths
            },
            status_code=200
        )

    except Exception as e:
        print("💥 Error in / route:", str(e))
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# ✅ Debug route (VERY useful)
@app.get("/debug")
def debug():
    try:
        return {
            "cwd": os.getcwd(),
            "base_dir": BASE_DIR,
            "files_in_cwd": os.listdir("."),
            "files_in_base_dir": os.listdir(BASE_DIR),
            "parent_dir_files": os.listdir(os.path.join(BASE_DIR, "..")),
        }
    except Exception as e:
        return {"error": str(e)}

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