import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column, relationship as sqlalchemy_relationship
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy.dialects.postgresql import UUID

import uuid

from src.repository.table import Base

class Application(Base):
    __tablename__ = "application"
    
    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    slug: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    job_id: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    
    # job = sqlalchemy_relationship("Job", back_populates="applicants")
    
    __mapper_args__ = {"eager_defaults": True}
    