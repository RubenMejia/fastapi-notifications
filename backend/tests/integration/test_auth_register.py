import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user import User

REGISTER_URL = "/api/auth/register"
VALID = {"email": "ana@example.com", "password": "S3cret-pass"}


async def test_register_returns_201_and_user(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json=VALID)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["email"] == "ana@example.com"
    assert "created_at" in body


async def test_register_duplicate_email_returns_409(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=VALID)

    response = await client.post(REGISTER_URL, json=VALID)

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


async def test_register_email_is_case_insensitive(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=VALID)

    response = await client.post(REGISTER_URL, json={**VALID, "email": "Ana@Example.com"})
    assert response.status_code == 409


async def test_register_short_password_returns_422(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json={**VALID, "password": "short"})

    assert response.status_code == 422


async def test_register_invalid_email_returns_422(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json={**VALID, "email": "not-an-email"})

    assert response.status_code == 422


async def test_register_unknown_field_returns_422(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json={**VALID, "is_admin": True})

    assert response.status_code == 422


# this is a way to test the same test with different parameters like Theory in XUnit
@pytest.mark.parametrize(
    "change",
    [{"password": "short"}, {"email": "not-an-email"}, {"is_admin": True}],
    ids=["short_password", "invalid_email", "unknown_field"],
)
async def test_register_invalid_body_returns_422(client: AsyncClient, change: dict) -> None:
    response = await client.post(REGISTER_URL, json={**VALID, **change})

    assert response.status_code == 422


async def test_register_response_has_no_password(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json=VALID)

    assert set(response.json()) == {"id", "email", "created_at"}


async def test_password_is_stored_hashed(client: AsyncClient, db: AsyncSession) -> None:
    await client.post(REGISTER_URL, json=VALID)

    user = await db.scalar(select(User).where(User.email == "ana@example.com"))

    assert user is not None
    assert user.hashed_password != VALID["password"]
    assert verify_password(VALID["password"], user.hashed_password)
