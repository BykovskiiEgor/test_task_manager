import uuid
import pytest
from datetime import datetime, timedelta

from task_manager.domain.models.task import Task, TaskStatus

def test_change_status_valid():
    t = Task(id=uuid.uuid4(), title="test")
    t.change_status(TaskStatus.IN_WORK)
    assert t.status == TaskStatus.IN_WORK
    assert hasattr(t, "updated_at") and isinstance(t.updated_at, datetime)

def test_change_status_invalid():
    t = Task(id=uuid.uuid4(), title="test", status=TaskStatus.COMPLETED)
    with pytest.raises(ValueError):
        t.change_status(TaskStatus.IN_WORK)

def test_is_overdue_true():
    t = Task(id=uuid.uuid4(), title="deadline", due_date=datetime.now() - timedelta(days=1))
    assert t.is_overdue is True

def test_is_overdue_false():
    t = Task(id=uuid.uuid4(), title="deadline", due_date=datetime.now() + timedelta(days=1))
    assert t.is_overdue is False

def test_is_overdue_none():
    t = Task(id=uuid.uuid4(), title="no due")
    assert t.is_overdue is False