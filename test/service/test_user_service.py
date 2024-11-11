# python unittest for user_service layer with mocking repository
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.schema.user_dto import UserCreate, UserUpdate, UserDTO
from app.security.jwt_token import JWTUser
from app.service.user_service import UserService
from unittest.mock import AsyncMock, patch
from app.schema.user_dto import UserDTO
from app.service.user_service import send_creation_email


# region init entity

def _get_jwt_user():
    return JWTUser(
        user_id="system",
        sub="system",
        email="system@system.com",
        scopes=["system"],
        expires=1000,
        token="token",
    )


def _get_create_entity():
    return UserCreate(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
        username="test",
        password="password",
    )


def _get_update_entity():
    return UserUpdate(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
    )


def _get_dto():
    return UserDTO(
        first_name="test",
        last_name="test",
        email="test@test.com",
        is_active=True,
        roles=["test"],
        user_id="test",
        username="test",
        created_by="system",
        created_date=datetime(2024, 1, 1),
        last_updated_by="system",
        last_updated_date=datetime(2024, 1, 1),
    )


def _get_service(repository):
    return UserService(user_repository=repository)


# endregion init entity


# success case for create
@pytest.mark.asyncio
async def test_given_valid_create_entity_when_create_then_return_dto():
    # Arrange 
    @pytest.mark.asyncio
    async def test_send_creation_email_success():
        # Arrange
        user = _get_dto()
        with patch("app.service.email_service.send_email", new_callable=AsyncMock) as mock_send_email:
            # Act
            await send_creation_email(user)

            # Assert
            mock_send_email.assert_called_once_with(
                "john.doe@example.com",
                "Welcome to the TestApp",
                "Hello John,\n\n"
                "Welcome to the TestApp. Your account has been created successfully.\n\n"
                "Please visit http://testapp.com to login to your account.\n\n"
                "TestApp Team."
            )


@pytest.mark.asyncio
async def test_send_creation_email_failure():
    # Arrange
    user = _get_dto()
    with patch("app.service.email_service.send_email", new_callable=AsyncMock) as mock_send_email:
        mock_send_email.side_effect = Exception("Email service failure")

        # Act
        with pytest.raises(Exception) as exc_info:
            await send_creation_email(user)

        # Assert
        assert str(exc_info.value) == "Email service failure"
        mock_send_email.assert_called_once_with(
            "john.doe@example.com",
            "Welcome to the TestApp",
            "Hello John,\n\n"
            "Welcome to the TestApp. Your account has been created successfully.\n\n"
            "Please visit http://testapp.com to login to your account.\n\n"
            "TestApp Team."
        )