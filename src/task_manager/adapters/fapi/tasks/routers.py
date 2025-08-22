from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from task_manager.adapters.db.connection import get_session
from task_manager.adapters.repository.task_repository import TaskRepository
from task_manager.applications.use_cases.task_crud import TaskCRUDUseCase
from task_manager.adapters.fapi.tasks.model import TaskResponse, TaskCreateRequest, TaskUpdateRequest, TaskStatusUpdate

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

async def get_task_usecase(db: AsyncSession = Depends(get_session)) -> TaskCRUDUseCase:
    repository = TaskRepository(db)
    return TaskCRUDUseCase(repository)

@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateRequest,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    try:
        task = await usecase.create_task(data=task_data)
        return TaskResponse.from_entity(task)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
    
@task_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    try:
        task = await usecase.get_task(task_id)
        return TaskResponse.from_entity(task)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdateRequest,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    try:
        task = await usecase.update_task(task_id=task_id, data=task_data)
        return TaskResponse.from_entity(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@task_router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    tasks = await usecase.get_all_tasks(skip, limit)
    return [TaskResponse.from_entity(task) for task in tasks]


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    try:
        await usecase.delete_task(task_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@task_router.patch("/{task_id}/status", response_model=TaskResponse)
async def change_task_status(
    task_id: UUID,
    status: TaskStatusUpdate,
    usecase: TaskCRUDUseCase = Depends(get_task_usecase)
):
    try:
        task = await usecase.change_task_status(task_id, status.status)
        return TaskResponse.from_entity(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))