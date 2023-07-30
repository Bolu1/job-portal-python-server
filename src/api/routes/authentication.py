import fastapi

from src.models.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken 
from src.repository.crud.user import UserCRUDRepository
from src.api.dependencies.repository import get_repository
from src.core.securites.authorizations.jwt import jwt_generator
from src.core.utils.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/user/signup",
    name="Auth: User Signup",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=UserInResponse
)
async def user_signup(
    user_create:UserInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository))
)-> UserInResponse:
    # check if email exists
    try:
       await user_repo.is_email_taken(email=user_create.email)
    except:
        raise await http_exc_400_credentials_bad_signup_request()
    
    # create account and access token
    new_account = await user_repo.create_account(user_create=user_create)
    access_token = jwt_generator.generate_access_token(user=new_account)
    
    # return response
    return UserInResponse(
        id= new_account.id,
        authorized_account=UserWithToken(
            token=access_token,
            slug=new_account.slug,
            resume_path=new_account.resume_path,
            is_admin=new_account.is_admin,
            email=new_account.email,  # type: ignore
            firstname=new_account.firstname,
            lastname=new_account.lastname,
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at, 
            updated_at=new_account.updated_at,
        )
    )
    
@router.post(
    "/admin/signup",
    name="Auth: Admin Signup",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=UserInResponse
)
async def admin_signup(
    user_create:UserInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository))
)-> UserInResponse:
    
    # check if user exists
    try:
        await user_repo.is_email_taken(email=user_create.email)
    except:
        raise await http_exc_400_credentials_bad_signup_request()

    # create account and access token
    new_account = await user_repo.create_account(user_create=user_create, is_admin=True)        
    access_token = jwt_generator.generate_access_token(user=new_account)
    
    # return response
    return UserInResponse(
        id= new_account.id,
        authorized_account=UserWithToken(
            token=access_token,
            slug=new_account.slug,
            resume_path=new_account.resume_path,
            is_admin=new_account.is_admin,
            email=new_account.email,  # type: ignore
            firstname=new_account.firstname,
            lastname=new_account.lastname,
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at, 
            updated_at=new_account.updated_at,
        )
    )
    
    
@router.post(
    "/signin",
    name="Auth: Signin",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=UserInResponse
)
async def signin(
    user_login:UserInLogin,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository))
)-> UserInResponse:
    try:
        logged_in_user = await user_repo.read_user_by_password_authentication(user_login=user_login)
    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()
    
    access_token = jwt_generator.generate_access_token(user=logged_in_user)
    
    return UserInResponse(
    id=logged_in_user.id,
    authorized_account=UserWithToken(
        token=access_token,
        slug=logged_in_user.slug,
        resume_path=logged_in_user.resume_path,
        is_admin=logged_in_user.is_admin,
        email=logged_in_user.email,  # type: ignore
        firstname=logged_in_user.firstname,
        lastname=logged_in_user.lastname,
        is_verified=logged_in_user.is_verified,
        is_active=logged_in_user.is_active,
        is_logged_in=logged_in_user.is_logged_in,
        created_at=logged_in_user.created_at,
        updated_at=logged_in_user.updated_at,
    ),
)