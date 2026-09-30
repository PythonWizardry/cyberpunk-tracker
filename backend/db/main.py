from sqlmodel import create_engine
from ..config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


engine = create_async_engine(
    settings.DATABASE_URL, 
    # echo=True,  #* shows sql code
    echo=False,
    future=True
)


async def get_session():
    # async_sessionmaker is the modern, recommended way for SQLAlchemy 2.0+
    Session = async_sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with Session() as session:
        yield session

