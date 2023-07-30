from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

# create base class for all crud classes
class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session
