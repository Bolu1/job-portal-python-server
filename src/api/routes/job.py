import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schemas.jwt import JWTAccount
from src.models.schemas.job import JobInCreate, JobInResponse, JobInUpdate
from src.repository.crud.job import JobCRUDRepository
from src.models.db.user import User
from src.core.securites.authorizations import oauth2
from src.core.utils.exceptions.http.exc_404 import(
    http_404_exc_id_not_found_request,
    http_404_exc_search_query_not_found_request
)

router = fastapi.APIRouter(prefix="/job", tags=["Jobs"])

@router.post(
    path="/",
    name="Jobs: Create Job",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=JobInResponse
)
async def create_job(
    job_create:JobInCreate,
    job_repo:JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository)),
    logged_in_user: User = fastapi.Depends(oauth2.get_logged_in_admin)
)-> JobInResponse :
    
    print(logged_in_user.is_admin)
    #call create job repository service
    new_job = await job_repo.create_job(job_create=job_create)
    
    # return response 
    return JobInResponse(
        id=new_job.id,
        slug=new_job.slug,
        title=new_job.title, 
        company_name=new_job.company_name, 
        city=new_job.city, 
        country=new_job.country, 
        salary=new_job.salary, 
        description=new_job.description,
        created_at=new_job.created_at,
        updated_at=new_job.updated_at
    )   
    
@router.get(
    "/",
    name="Jobs: Read Jobs",
    response_model=list[JobInResponse],
    status_code=fastapi.status.HTTP_200_OK
)
async def get_jobs(job_repo: JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository)))-> list[JobInResponse]:
    # read jobs from 
    db_jobs = await job_repo.read_jobs()
    return db_jobs

@router.get(
    "/{id}",
    name="Jobs: Read Job By Id",
    response_model=JobInResponse,
    status_code=fastapi.status.HTTP_200_OK
)
async def get_job(
    id: str,
    job_repo: JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository))
)-> JobInResponse:
    #read job by id
    try:
        db_job = await job_repo.read_job(id=id)
    except Exception:
        raise await http_404_exc_id_not_found_request(id=id)
    
    return JobInResponse(
        id=db_job.id,
        slug=db_job.slug,
        title=db_job.title, 
        company_name=db_job.company_name, 
        city=db_job.city, 
        country=db_job.country, 
        salary=db_job.salary, 
        description=db_job.description,
        created_at=db_job.created_at,
        updated_at=db_job.updated_at
    )
    
@router.get(
    "/search/{search_query}",
    name="Jobs: Search Job",
    response_model=JobInResponse,
    status_code=fastapi.status.HTTP_200_OK
)
async def search_job(
    search_query: str = "",
    job_repo: JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository))
)-> JobInResponse:
    #search job by query
    
    try:
        db_job = await job_repo.search_job_by_query(search_query=search_query)
    except Exception:
        raise await http_404_exc_search_query_not_found_request(search_query=search_query)
    
    return JobInResponse(
        id=db_job.id,
        slug=db_job.slug,
        title=db_job.title, 
        company_name=db_job.company_name, 
        city=db_job.city, 
        country=db_job.country, 
        salary=db_job.salary, 
        description=db_job.description,
        created_at=db_job.created_at,
        updated_at=db_job.updated_at
    )
 
@router.patch(
    "/{id}",
    name="Jobs: Edit Job",
    response_model=JobInResponse,
    status_code=fastapi.status.HTTP_200_OK
)   
async def update_job(
    id: int,
    job_update:JobInUpdate,
    job_repo: JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository)),
    logged_in_user: User = fastapi.Depends(oauth2.get_logged_in_admin)
)->JobInResponse:
    try:
        updated_db_job = await job_repo.update_job_by_id(id=id, job_update=job_update)
        
    except Exception:
        raise await http_404_exc_id_not_found_request(id=id)
    
    return JobInResponse(
        id=updated_db_job.id,
        slug=updated_db_job.slug,
        title=updated_db_job.title, 
        company_name=updated_db_job.company_name, 
        city=updated_db_job.city, 
        country=updated_db_job.country, 
        salary=updated_db_job.salary, 
        description=updated_db_job.description,
        created_at=updated_db_job.created_at,
        updated_at=updated_db_job.updated_at
    )
    
@router.delete(
    "/{id}",
    name="Jobs: Delete Job",
    status_code=fastapi.status.HTTP_200_OK
)
async def delete_job(
    id: int,
    job_repo: JobCRUDRepository = fastapi.Depends(get_repository(repo_type=JobCRUDRepository)),
    logged_in_user: User = fastapi.Depends(oauth2.get_logged_in_admin)
)-> str:
    try:
        deletion_result = await job_repo.delete_job_by_id(id=id)
        
    except Exception:
        raise await http_404_exc_id_not_found_request(id=id)
    
    return deletion_result
    
