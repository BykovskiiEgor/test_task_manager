import pytest
from task_manager.adapters.repository.task_repository import TaskRepository
from task_manager.domain.dto.task import CreateTaskDTO

@pytest.mark.asyncio
async def test_repository_crud_flow(db_session):
    repo = TaskRepository(db_session)

    created = await repo.create(CreateTaskDTO(title="db task", description="d"))
    assert created.id is not None
    assert created.title == "db task"

    got = await repo.get_by_id(created.id)
    assert got is not None and got.id == created.id

    got.title = "updated"
    saved = await repo.update(got)
    assert saved.title == "updated"

    items = await repo.get_all()
    assert any(i.id == created.id for i in items)

    deleted = await repo.delete(created.id)
    assert deleted is True

    missing = await repo.get_by_id(created.id)
    assert missing is None