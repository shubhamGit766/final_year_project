from fastapi import Header, HTTPException
from auth_service import decode_access_token


async def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Use this as a dependency on any protected route:
    current_user: dict = Depends(get_current_user)
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header format")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"user_id": payload["sub"], "email": payload["email"]}