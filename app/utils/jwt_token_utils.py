def get_username_from_jwt_token(token_data: dict):
    return token_data["sub"]
