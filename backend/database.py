import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = "resume_interview_app"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
resumes_collection = db["resumes"]