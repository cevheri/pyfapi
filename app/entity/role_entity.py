from beanie import Document


class Role(Document):
    name: str

    # constructor
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    class Settings:
        collection = "app_role"
