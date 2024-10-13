from beanie import Document


class Role(Document):
    name: str

    class Settings:
        collection = "app_role"
