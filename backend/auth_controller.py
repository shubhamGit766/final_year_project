from datetime import datetime
from bson import ObjectId
from database import users_collection
from auth_service import hash_password, verify_password, create_access_token


async def register_user(name: str, email: str, password: str) -> dict:
    print(f"[AUTH] Registering user: {email}")

    # Check if email already exists
    existing = await users_collection.find_one({"email": email})
    if existing:
        return {"error": "Email already registered"}

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "",
        "level": "",
        "created_at": datetime.utcnow(),
    }

    result = await users_collection.insert_one(user)
    user_id = str(result.inserted_id)

    token = create_access_token(user_id, email)
    print(f"[AUTH] User registered: {email}")
    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": "",
            "level": "",
        }
    }


async def login_user(email: str, password: str) -> dict:
    print(f"[AUTH] Login attempt: {email}")

    user = await users_collection.find_one({"email": email})
    if not user:
        return {"error": "Invalid email or password"}

    if not verify_password(password, user["password"]):
        return {"error": "Invalid email or password"}

    user_id = str(user["_id"])
    token = create_access_token(user_id, email)
    print(f"[AUTH] Login successful: {email}")
    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": user.get("name", ""),
            "email": email,
            "role": user.get("role", ""),
            "level": user.get("level", ""),
        }
    }


async def update_profile(user_id: str, role: str, level: str) -> dict:
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": role, "level": level}}
    )
    return {"message": "Profile updated"}