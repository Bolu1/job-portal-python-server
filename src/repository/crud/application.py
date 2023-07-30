import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions


from src.models.db.application import Application
from src.models.schemas.user import UserInCreate, UserInLogin
from src.core.securites.hashing.password import pwd_generator
from src.core.utils.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.models.schemas.job import JobInCreate, JobInUpdate
from src.models.db.job import Job

from src.repository.crud.base import BaseCRUDRepository

class ApplicationCRUDRepository(BaseCRUDRepository):
    async def create_application(
        self,
        job_id: str,
        user_id: int
    )-> Application:
        #create application
        new_application_payload = Application(job_id=job_id, user_id=user_id)
        
        self.async_session.add(instance=new_application_payload)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_application_payload)
        
        return new_application_payload
    
    async def is_application_exists(
        self,
        job_id:str,
        user_id:str
    )-> bool:
        query_statement = sqlalchemy.select(Application.id).where(Application.job_id== job_id , Application.user_id == user_id)
        query = await self.async_session.execute(statement=query_statement)
        
        fetched_application_id = query.scalar()
        
        if fetched_application_id:
            raise EntityAlreadyExists("Application already exists")
        
        return True 
        
        