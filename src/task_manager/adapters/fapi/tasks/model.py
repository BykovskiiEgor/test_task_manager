from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from task_manager.domain.models.task import Task

class TaskStatusUpdate(BaseModel):
    status: str = Field(..., description="Новый статус задачи")
    

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    status_display: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[date]
    is_overdue: bool

    @classmethod
    def from_entity(cls, task: Task) -> 'TaskResponse':
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            status_display=task.status.display_names,
            created_at=task.created_at,
            updated_at=task.updated_at or task.created_at,
            due_date=task.due_date,
            is_overdue=task.is_overdue
        )

