from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Mount static ONLY if exists
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "API is running"}

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