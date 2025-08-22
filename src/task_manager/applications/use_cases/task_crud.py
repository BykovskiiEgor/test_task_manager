from uuid import UUID

from task_manager.applications.interfaces.repository import ITaskRepository
from task_manager.domain.dto.task import CreateTaskDTO, UpdateTaskDTO
from task_manager.domain.exceptions.task import TaskNotFoundError, TaskValidationError
from task_manager.domain.models.task import Task, TaskStatus


class TaskCRUDUseCase:

    def __init__(self, task_repository: ITaskRepository):
        self.task_repo = task_repository


    async def create_task(self, data: CreateTaskDTO) -> Task:
        if not data.title.strip():
            raise TaskValidationError("Название не может быть пустым")
        return await self.task_repo.create(data)


    async def get_task(self, task_id: UUID) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Задача с ID {task_id} не найдена")
        return task


    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        return await self.task_repo.get_all(skip, limit)


    async def update_task(self, task_id: UUID, data: UpdateTaskDTO) -> Task:
        task = await self.task_repo.get_by_id(task_id)

        if data.title is not None:
            if not data.title.strip():
                raise TaskValidationError("Название не должно быть пустым")
            task.title = data.title.strip()

        if data.description is not None:
            task.description = data.description

        if data.due_date is not None:
            task.due_date = data.due_date

        return await self.task_repo.update(task)


    async def change_task_status(self, task_id: UUID, new_status: TaskStatus) -> Task:
        task = await self.get_task(task_id)
        task.change_status(new_status)
        return await self.task_repo.update(task)


    async def get_task_by_status(self, status: TaskStatus) -> list[Task]:
        return await self.task_repo.get_by_status(status)
    
    
    async def delete_task(self, task_id: UUID) -> None:
        if not await self.task_repo.delete(task_id):
            raise TaskNotFoundError(f"Задача с ID {task_id} не найдена для удаления")
