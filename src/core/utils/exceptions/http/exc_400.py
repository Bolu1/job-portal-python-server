"""
The HyperText Transfer Protocol (HTTP) 400 Bad Request response status code indicates that the server
cannot or will not process the request due to something that is perceivedto be a client error
(for example, malformed request syntax, invalid request message framing, or deceptive request routing).
"""

import fastapi

from src.core.utils.messages.exceptions.http.exc_details import (
    http_400_sigin_credentials_details,
    http_400_signup_credentials_details,
    http_400_duplicate_bad_application_details,
)


async def http_exc_400_credentials_bad_signup_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_signup_credentials_details(),
    )


async def http_exc_400_credentials_bad_signin_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_sigin_credentials_details(),
    )


async def http_400_exc_duplicate_bad_application_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_duplicate_bad_application_details(),
    )

