from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = False
    data: dict = None
    message: str = None
    error: str = None
