import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

print("🚀 App starting...")

BASE_DIR = os.getcwd()
print(f"📁 BASE_DIR: {BASE_DIR}")

# Debug files
try:
    print(f"📂 Files: {os.listdir(BASE_DIR)}")
except Exception as e:
    print(f"❌ Error reading dir: {e}")


@app.get("/")
def root():
    try:
        index_path = os.path.join(BASE_DIR, "index.html")
        print(f"📄 Serving: {index_path}")

        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            return JSONResponse(
                status_code=404,
                content={"error": "index.html not found"}
            )

    except Exception as e:
        print(f"❌ ERROR in / route: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# VERY IMPORTANT for Railway health
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