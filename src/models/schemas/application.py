import datetime

import pydantic
import uuid

from src.models.schemas.base import BaseSchemaModel   
    
class ApplicationInResponse(BaseSchemaModel):
    id: int
    slug: uuid.UUID
    job_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None