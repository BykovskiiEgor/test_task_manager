from abc import ABC, abstractmethod
from uuid import UUID

from task_manager.domain.dto.task import CreateTaskDTO, UpdateTaskDTO
from task_manager.domain.models.task import Task, TaskStatus


class ITaskRepository(ABC):


    @abstractmethod
    async def create(self, tak: CreateTaskDTO) -> Task:
        pass


    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task:
        pass


    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        pass


    @abstractmethod
    async def update(self, task: UpdateTaskDTO) -> Task:
        pass


    @abstractmethod
    async def delete(self, task_id: UUID) -> bool:
        pass


    @abstractmethod
    async def get_by_status(self, status: TaskStatus) -> list[Task]:
        pass
