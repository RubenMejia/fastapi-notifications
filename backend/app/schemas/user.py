from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field

# EmailStr lowercases only the domain; emails are unique case-insensitively, so lowercase it all
Email = Annotated[EmailStr, AfterValidator(str.lower)]


class UserCreate(BaseModel):
    # forbid: means that any extra fields will be rejected
    model_config = ConfigDict(extra="forbid")

    email: Email
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    # from_attributes: means the model will be converted to a dictionary and then back to a model,
    # like a automapper, read the sqlalchemy model and convert to a pydantic model
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str  # output comes from the database, it doesnt need to be validated again
    created_at: datetime
