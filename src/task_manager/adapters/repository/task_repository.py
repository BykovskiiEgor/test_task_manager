from uuid import UUID
from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.adapters.models.task_model import Task, TaskStatus
from task_manager.applications.interfaces.repository import ITaskRepository
from task_manager.domain.dto.task import CreateTaskDTO


class TaskRepository(ITaskRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, dto: CreateTaskDTO) -> Task:
        task = Task(
            title=dto.title,
            description=dto.description,
            due_date=dto.due_date
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update(self, task: Task) -> Task:
        self.session.add(task)           
        await self.session.commit()      
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        stmt = select(Task).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, task_id: UUID) -> bool:
        stmt = delete(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_status(self, status: TaskStatus) -> List[Task]:
        stmt = select(Task).where(Task.status == status.value)
        result = await self.session.execute(stmt)
        return result.scalars().all()
