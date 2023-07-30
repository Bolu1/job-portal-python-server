import datetime

import pydantic
import uuid

from src.models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    email: pydantic.EmailStr
    password: str
    firstname: str
    lastname: str


class UserInUpdate(BaseSchemaModel):
    email: str | None
    password: str | None


class UserInLogin(BaseSchemaModel):
    email: pydantic.EmailStr
    password: str


class UserWithToken(BaseSchemaModel):
    token: str
    slug: uuid.UUID
    is_admin: bool
    email: pydantic.EmailStr
    firstname: str
    lastname: str
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    resume_path: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UserInResponse(BaseSchemaModel):
    id: int
    authorized_account: UserWithToken
