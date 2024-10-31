from beanie import Document


class Role(Document):
    name: str

    class Settings:
        name = "app_role"
