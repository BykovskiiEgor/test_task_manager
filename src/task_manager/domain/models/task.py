import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    CREATED = 'Создана'
    IN_WORK = 'В работе'
    COMPLETED = 'Завершена'

    @property
    def display_names(self) -> str:
        names = {
            self.CREATED: 'Создана',
            self.IN_WORK: 'В работе', 
            self.COMPLETED: 'Завершена',
        }
        return names[self]

    def can_transition_to(self, new_status: 'TaskStatus') -> bool:
        allowed_transitions = {
            self.CREATED: [self.IN_WORK, self.COMPLETED],
            self.IN_WORK: [self.COMPLETED],
            self.COMPLETED: [],
        }
        return new_status in allowed_transitions[self]


@dataclass
class Task:
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    status:  TaskStatus = TaskStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

    def change_status(self, new_status: TaskStatus) -> None:
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"Недопустимый переход статуса: {self.status.display_names} -> {new_status.display_names}"
            )
        self.status = new_status
        self.updated_at = datetime.now()

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        if isinstance(self.due_date, datetime):
            due = self.due_date.date()
        else:
            due = self.due_date

        return date.today() > due
