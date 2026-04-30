from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.settings import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async_session = async_session_maker

Base = declarative_base()


async def get_db():
    """Dependency для FastAPI - обеспечивает сессию БД"""
    async with async_session_maker() as session:
        yield session
