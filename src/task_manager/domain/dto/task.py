from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CreateTaskDTO:
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None


@dataclass
class UpdateTaskDTO:
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
