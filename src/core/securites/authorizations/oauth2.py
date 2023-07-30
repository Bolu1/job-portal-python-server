from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.securites.authorizations.jwt import jwt_generator
from  src.repository.crud.user import UserCRUDRepository
from src.api.dependencies.repository import get_repository
from src.core.utils.exceptions.http.exc_403 import http_exc_403_forbidden_request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

async def get_logged_in_admin(token:str = Depends(oauth2_scheme), user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository))):

    # check if token is valid and read user information
    logged_in_user = jwt_generator.retrieve_details_from_token(token)
    logged_in_user_details = await user_repo.read_user_by_id(id=logged_in_user.id) 
    
    # check if user is an admin
    if not logged_in_user_details.is_admin:
        raise await http_exc_403_forbidden_request()
    
    return logged_in_user_details