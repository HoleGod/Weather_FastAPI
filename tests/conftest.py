import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
@pytest.fixture
async def async_session(async_engine):
    SessionLocal = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session
        
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, async_session):
    async def _override_get_db():
        yield async_session

    monkeypatch.setattr("app.core.database.get_db", _override_get_db)