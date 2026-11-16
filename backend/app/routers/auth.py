from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.db.session import DbSession
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


# Dependency injection function, like a constructor
def get_auth_service(db: DbSession) -> AuthService:
    return AuthService(UserRepository(db))


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"description": "Email already registered"}},
)
async def register(data: UserCreate, service: AuthServiceDependency) -> UserResponse:
    user = await service.register(data)
    return UserResponse.model_validate(user)
