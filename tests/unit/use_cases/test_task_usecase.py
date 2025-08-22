import uuid
import pytest
from unittest.mock import AsyncMock

from task_manager.applications.use_cases.task_crud import TaskCRUDUseCase
from task_manager.domain.dto.task import CreateTaskDTO, UpdateTaskDTO
from task_manager.domain.models.task import Task, TaskStatus
from task_manager.domain.exceptions.task import TaskNotFoundError, TaskValidationError

@pytest.mark.asyncio
async def test_create_task_success():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    dto = CreateTaskDTO(title=" ok ", description="d")
    task = Task(id=uuid.uuid4(), title="ok", description="d")
    repo.create.return_value = task

    result = await uc.create_task(dto)
    assert result.title == "ok"
    repo.create.assert_awaited()

@pytest.mark.asyncio
async def test_create_task_empty_title():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    dto = CreateTaskDTO(title="   ")
    with pytest.raises(TaskValidationError):
        await uc.create_task(dto)

@pytest.mark.asyncio
async def test_get_task_found():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    task_id = uuid.uuid4()
    repo.get_by_id.return_value = Task(id=task_id, title="t")

    result = await uc.get_task(task_id)
    assert result.id == task_id

@pytest.mark.asyncio
async def test_get_task_not_found():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    repo.get_by_id.return_value = None
    with pytest.raises(TaskNotFoundError):
        await uc.get_task(uuid.uuid4())

@pytest.mark.asyncio
async def test_update_task_changes():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    task_id = uuid.uuid4()
    existing = Task(id=task_id, title="old", description="x")
    repo.get_by_id.return_value = existing
    repo.update.return_value = existing

    dto = UpdateTaskDTO(title="  new  ", description="y")
    result = await uc.update_task(task_id, dto)
    assert result.title == "new"
    assert result.description == "y"
    repo.update.assert_awaited_with(existing)

@pytest.mark.asyncio
async def test_update_task_empty_title_fails():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    task_id = uuid.uuid4()
    existing = Task(id=task_id, title="old")
    repo.get_by_id.return_value = existing

    dto = UpdateTaskDTO(title="   ")
    with pytest.raises(TaskValidationError):
        await uc.update_task(task_id, dto)

@pytest.mark.asyncio
async def test_change_task_status_success():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    task_id = uuid.uuid4()
    task = Task(id=task_id, title="t")
    repo.get_by_id.return_value = task
    repo.update.return_value = task

    result = await uc.change_task_status(task_id, TaskStatus.IN_WORK)
    assert result.status == TaskStatus.IN_WORK

@pytest.mark.asyncio
async def test_delete_task_not_found():
    repo = AsyncMock()
    uc = TaskCRUDUseCase(repo)
    repo.delete.return_value = False
    with pytest.raises(Exception):
        await uc.delete_task(uuid.uuid4())

