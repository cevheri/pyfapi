from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = False
    data: dict = None
    status_code: str = None
    message: str = None

response_status_codes = {
    200: {"description": "Success"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not Found"},
    500: {"description": "Internal Server Error"}
}