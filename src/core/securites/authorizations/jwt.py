import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from src.core.config.manager import settings
from src.models.db.user import User
from src.models.schemas.jwt import JWTAccount, JWToken
from src.core.utils.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta

        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_MIN)

        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

        return jose_jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def generate_access_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(f"Cannot generate JWT token for without user entity!")

        return self._generate_jwt_token(
            jwt_data=JWTAccount(id=user.id, email=user.email).dict(),  # type: ignore
            expires_delta=datetime.timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

    def retrieve_details_from_token(self, token: str) -> list[str]:
        try:
            payload = jose_jwt.decode(token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            jwt_account = JWTAccount(id=payload["id"], email=payload["email"])

        except JoseJWTError as token_decode_error:
            raise ValueError("Unable to decode JWT Token") from token_decode_error

        except pydantic.ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return jwt_account


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
