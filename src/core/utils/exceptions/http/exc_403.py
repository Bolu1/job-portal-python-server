"""
The HTTP 403 Forbidden response status code indicates that the server understands the request but refuses to authorize it.
"""

import fastapi

from src.core.utils.messages.exceptions.http.exc_details import http_403_forbidden_details


async def http_exc_403_forbidden_request() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_403_FORBIDDEN,
        detail=http_403_forbidden_details(),
    )
