import datetime

import pydantic


class JWToken(pydantic.BaseModel):
    exp: datetime.datetime
    sub: str


class JWTAccount(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
