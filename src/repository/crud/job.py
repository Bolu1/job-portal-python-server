import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions


from src.models.db.user import User
from src.models.schemas.user import UserInCreate, UserInLogin
from src.core.securites.hashing.password import pwd_generator
from src.core.utils.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.models.schemas.job import JobInCreate, JobInUpdate
from src.models.db.job import Job

from src.repository.crud.base import BaseCRUDRepository

class JobCRUDRepository(BaseCRUDRepository):
    async def create_job(
        self,
        job_create: JobInCreate
        )-> Job:
        # create job payload
        new_job_payload = Job(title=job_create.title, company_name=job_create.company_name, city=job_create.city, country=job_create.country, salary=job_create.salary, description=job_create.description)
        
        self.async_session.add(instance=new_job_payload)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_job_payload)
        
        return new_job_payload
    
    async def read_jobs(self)-> typing.Sequence[Job]:
        query_statement = sqlalchemy.select(Job).order_by(Job.created_at.desc())
        query = await self.async_session.execute(statement=query_statement)
        return query.scalars().all()
    
    async def read_job(
        self,
        id:str
    )-> Job:
        query_statement = sqlalchemy.select(Job).where(Job.slug == id)
        query = await self.async_session.execute(statement=query_statement)
        
        fetched_job = query.scalar()
        
        if not fetched_job:
            raise EntityDoesNotExist("Job with id `{id}` does not exist!")
        
        return fetched_job
    
    async def search_job_by_query(
        self,
        search_query:str
    )-> Job:
        query_statement = sqlalchemy.select(Job).where(Job.title.like(search_query))
        print(search_query)
        query = await self.async_session.execute(statement=query_statement)
        
        fetched_job = query.all()
        
        if not fetched_job:
            raise EntityDoesNotExist("Job with id `{id}` does not exist!")
        
        return fetched_job
        
    async def update_job_by_id(self, id:int, job_update:JobInUpdate)-> Job:
        new_job_data = job_update.model_dump()
        
        # select job details by id
        query_statement = sqlalchemy.select(Job).where(Job.id == id)
        query = await self.async_session.execute(statement=query_statement)
        update_job = query.scalar()
        
        if not update_job:
            raise EntityDoesNotExist(f"Job with id `{id}` does not exist!")
        
        update_statement = sqlalchemy.update(table=Job).where(Job.id == update_job.id).values(updated_at=sqlalchemy_functions.now())
        
        if new_job_data["title"]:
            update_statement = update_statement.values(title=new_job_data["title"])
        if new_job_data["company_name"]:
            update_statement = update_statement.values(company_name=new_job_data["company_name"])
        if new_job_data["city"]:
            update_statement = update_statement.values(city=new_job_data["city"])
        if new_job_data["country"]:
            update_statement = update_statement.values(country=new_job_data["country"])
        if new_job_data["salary"]:
            update_statement = update_statement.values(salary=new_job_data["salary"])
        if new_job_data["description"]:
            update_statement = update_statement.values(description=new_job_data["description"])
            
        await self.async_session.execute(statement=update_statement)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_job)
        
        return update_job
    
    async def delete_job_by_id(self, id:int)-> str:
        select_statement = sqlalchemy.select(Job).where(Job.id == id)
        query = await self.async_session.execute(statement=select_statement)
        delete_job = query.scalar()
        
        if not delete_job:
            raise EntityDoesNotExist(f"Job with id `{id}` does not exist!") 
        
        query_statement = sqlalchemy.delete(table=Job).where(Job.id == delete_job.id)
        
        await self.async_session.execute(statement=query_statement)
        await self.async_session.commit()
        
        return f"Job with id '{id}' is successfully deleted!"