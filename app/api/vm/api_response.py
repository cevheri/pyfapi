from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = False
    data: dict = None
    status_code: str = None
    message: str = None
