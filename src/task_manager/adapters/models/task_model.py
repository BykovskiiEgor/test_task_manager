import uuid
from datetime import date, datetime
from enum import Enum
from typing import Annotated, Optional

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from task_manager.adapters.db.connection import Base


class TaskStatus(Enum):
    CREATED = 'created'
    IN_WORK = 'in_work'
    COMPLETED = 'completed'

    @property
    def display_names(self) -> str:
        names = {
            TaskStatus.CREATED: 'Создана',
            TaskStatus.IN_WORK: 'В работе',
            TaskStatus.COMPLETED: 'Завершена',
        }

        return names[self]


    def can_change_to(self, new_status: 'TaskStatus') -> bool:
        allowed_changes = {
            TaskStatus.CREATED: [TaskStatus.IN_WORK, TaskStatus.COMPLETED],
            TaskStatus.IN_WORK: [TaskStatus.COMPLETED],
            TaskStatus.COMPLETED: [],
        }
        return new_status in allowed_changes[self]

created_at = Annotated[datetime, mapped_column(DateTime, server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=func.now(), onupdate=func.now())]


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus, name='task_status_enum'),
        default=TaskStatus.CREATED,
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    
    
    def change_status(self, new_status: TaskStatus):
        if not isinstance(new_status, TaskStatus):
            new_status = TaskStatus(new_status)  
        if not self.status.can_change_to(new_status):
            raise ValueError(f"Недопустимый переход статуса: {self.status.display_names} -> {new_status.display_names}")
        self.status = new_status
    
    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        if isinstance(self.due_date, datetime):
            due = self.due_date.date()
        else:
            due = self.due_date

        return date.today() > due
    
    
