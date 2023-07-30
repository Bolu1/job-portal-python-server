import datetime

import pydantic
import uuid

from src.models.schemas.base import BaseSchemaModel

class JobInCreate(BaseSchemaModel):
    title: str
    company_name: str
    city: str
    country: str
    city: str
    country: str
    salary: str
    description: str
    
class JobInUpdate(BaseSchemaModel):
    title: str
    company_name: str
    city: str
    country: str
    city: str
    country: str
    salary: str
    description: str
    
class JobInResponse(BaseSchemaModel):
    id: int
    title: str
    company_name: str
    city: str
    country: str
    slug: uuid.UUID
    country: str
    salary: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None