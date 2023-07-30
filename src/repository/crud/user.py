import typing

import sqlalchemy
from src.core.securites.verifications.credentials import credential_verifier
from sqlalchemy.sql import functions as sqlalchemy_functions
from src.models.db.user import User
from src.models.schemas.user import UserInCreate, UserInLogin
from src.core.securites.hashing.password import pwd_generator
from src.core.utils.exceptions.database import EntityAlreadyExists, EntityDoesNotExist

from src.repository.crud.base import BaseCRUDRepository

class UserCRUDRepository(BaseCRUDRepository):
    async def is_email_taken(self, email:str)-> bool:
        email_statement = sqlalchemy.select(User.email).select_from(User).where(User.email == email)
        email_query = await self.async_session.execute(email_statement)
        db_email = email_query.scalar()
        
        if not credential_verifier.is_email_available(email=db_email):
            raise EntityAlreadyExists(message=f"The email `{email}` is already registered!")
        
        return True
    
    async def read_user_by_id(self, id:int)-> User: 
        query_statement = sqlalchemy.select(User).where(User.id == id)
        query = await self.async_session.execute(statement=query_statement)
        
        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")
        
        return query.scalar()
        
    async def create_account(self, user_create: UserInCreate, is_admin:bool = False)-> User:
        print(user_create.firstname, user_create.lastname)
        new_user_payload = User(email=user_create.email, is_logged_in=True, is_admin=is_admin, firstname=user_create.firstname, lastname=user_create.lastname)
        
        new_user_payload.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        password_hash = pwd_generator.generate_hashed_password(
                hash_salt=new_user_payload.hash_salt, new_password=user_create.password
            )
        new_user_payload.set_hashed_password(
            hashed_password= password_hash
        )
        
        self.async_session.add(instance=new_user_payload)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user_payload)
        
        return new_user_payload
    
    async def read_user_by_password_authentication(self, user_login:UserInLogin)-> User:
        query_statement = sqlalchemy.select(User).select_from(User).where(
            User.email == user_login.email
        )
        query = await self.async_session.execute(statement=query_statement)
        fetched_account = query.scalar()
        
        if not fetched_account:
            raise EntityDoesNotExist("Invalid login details!")
        
        if not pwd_generator.is_password_authenticated(hash_salt=fetched_account.hash_salt, password=user_login.password, hashed_password=fetched_account.hashed_password):
            raise EntityDoesNotExist("Invalid login details")
        
        return fetched_account
    
    
    