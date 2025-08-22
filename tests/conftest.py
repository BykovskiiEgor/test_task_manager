import asyncio
import uuid
import pytest
from datetime import date, timedelta
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from task_manager.main.web import create_app
from task_manager.adapters.db.connection import get_session as app_get_session
from task_manager.adapters.models.task_model import Base as ORMBase



DATABASE_URL = "postgresql+asyncpg://test_user:test_password@db_test:5432/task_manager_test"

@pytest.fixture(scope="session")
def event_loop():
    """Создаем новый event loop для pytest-asyncio."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(ORMBase.metadata.drop_all)
        await conn.run_sync(ORMBase.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with test_engine.begin() as conn:
        async with conn.begin_nested():  
            async with async_session(bind=conn) as session:
                yield session
                await session.rollback()


@pytest_asyncio.fixture
async def app(db_session):
    """Создаем тестовое приложение FastAPI с подмененной зависимостью сессии."""
    app = create_app()

    async def _override_session():
        yield db_session

    app.dependency_overrides[app_get_session] = _override_session
    return app

@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


def _detect_status_values():
    from task_manager.domain.models.task import TaskStatus as DomainStatus
    values = {name: member.value for name, member in DomainStatus.__members__.items()}

    return {
        "created": values.get("CREATED", "created"),
        "in_work": values.get("IN_WORK", "in_work"),
        "completed": values.get("COMPLETED", "completed"),
    }


@pytest.fixture(scope="session")
def status_values():
    return _detect_status_values()


@pytest.fixture
def task_payload():
    return {
        "title": "Тестовая задача",
        "description": "Описание задачи",
        "due_date": (date.today() + timedelta(days=1)).isoformat()
    }


@pytest.fixture
def update_payload():
    return {
        "title": "Обновлённый заголовок",
        "description": "Новое описание",
        "due_date": (date.today() + timedelta(days=1)).isoformat()
    }


@pytest.fixture
def random_uuid():
    return uuid.uuid4()
