"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

import fastapi

from src.core.utils.messages.exceptions.http.exc_details import (
    http_404_email_details,
    http_404_id_details,
    http_404_search_query_details,
)


async def http_404_exc_email_not_found_request(email: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_email_details(email=email),
    )


async def http_404_exc_id_not_found_request(id: int) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(id=id),
    )


async def http_404_exc_search_query_not_found_request(search_query: str) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_search_query_details(search_query=search_query),
    )
