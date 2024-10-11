from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")

@router.get("/users")
def get_users():
    return {"users": "users"}