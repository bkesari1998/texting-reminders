from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Task


class TaskRepository:
    """Repository for Task database operations."""

    @staticmethod
    def get_all_tasks(db: Session) -> list[Task]:
        """Get all tasks from the database."""
        stmt = select(Task)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_incomplete_tasks(db: Session) -> list[Task]:
        """Get all incomplete tasks from the database."""
        stmt = select(Task).where(Task.completed == False)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_completed_tasks(db: Session) -> list[Task]:
        """Get all completed tasks from the database."""
        stmt = select(Task).where(Task.completed == True)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task | None:
        """Get a task by its ID."""
        stmt = select(Task).where(Task.id == task_id)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    def create_task(
        db: Session,
        description: str,
        deadline_date: date | None = None,
        deadline_time: time | None = None
    ) -> Task:
        """Create a new task.

        If deadline_time is provided without deadline_date,
        deadline_date will be set to today.
        """
        # Business logic: if time is set without date, use today's date
        if deadline_time and not deadline_date:
            deadline_date = date.today()

        task = Task(
            description=description,
            deadline_date=deadline_date,
            deadline_time=deadline_time
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def toggle_task_completion(db: Session, task_id: int) -> Task | None:
        """Toggle the completion status of a task.

        Returns the updated task if found, None otherwise.
        """
        task = TaskRepository.get_task_by_id(db, task_id)
        if task:
            task.completed = not task.completed
            db.commit()
            db.refresh(task)
            return task
        return None
