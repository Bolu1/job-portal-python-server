import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.jwt import JWTAccount
from src.models.schemas.job import JobInCreate, JobInResponse, JobInUpdate
from src.repository.crud.application import ApplicationCRUDRepository
from src.models.db.user import User
from src.models.db.application import Application
from src.models.schemas.application import ApplicationInResponse
from src.core.securites.authorizations import oauth2

from src.core.utils.exceptions.http.exc_400 import(
    http_400_exc_duplicate_bad_application_request
)


router = fastapi.APIRouter(prefix="/application", tags=["Applications"])

@router.post(
    path="/{job_id}",
    name="Applications: Create Applications",
    status_code=fastapi.status.HTTP_201_CREATED
)
async def create_application(
    job_id: str,
    application_repo:ApplicationCRUDRepository = fastapi.Depends(get_repository(repo_type=ApplicationCRUDRepository)),
    logged_in_user: User = fastapi.Depends(oauth2.get_logged_in_admin)
):
    #check if application exists
    try:
        await application_repo.is_application_exists(job_id=job_id, user_id=logged_in_user.slug)
    except Exception:
        raise await http_400_exc_duplicate_bad_application_request()
    
    new_application = await application_repo.create_application(job_id=job_id, user_id=logged_in_user.slug)
    
    return ApplicationInResponse(
        id= new_application.id,
        slug= new_application.slug,
        job_id= new_application.job_id,
        user_id= new_application.user_id,
        created_at= new_application.created_at,
        updated_at= new_application.updated_at
    )