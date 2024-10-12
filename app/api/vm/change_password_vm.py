from pydantic import BaseModel


class ChangePasswordVM(BaseModel):
    current_password: str
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "plain-text-current-password",
                "new_password": "plain-text-new-password"
            }
        }