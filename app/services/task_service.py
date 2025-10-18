from app.repository.task_repository import TaskRepository
from datetime import date
from app.models import TaskStatus

class BusinessException(Exception):
    pass

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, dto):
        if not dto.title.strip():
            raise BusinessException("Title cannot be empty")
       # if dto.due_date and dto.due_date < date.today():
        #    raise BusinessException("Due date cannot be in the past")
        return self.repo.create(dto.title, dto.description, dto.due_date)

    def list_tasks(self, status=None):
        return self.repo.list(status)

    def update_status(self, task_id, new_status):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise BusinessException("Task not found")

        
        valid_statuses = [TaskStatus.pending.value, TaskStatus.in_progress.value, TaskStatus.done.value]
        if new_status not in valid_statuses:
            raise BusinessException("Invalid status value")

        
        if task.status == TaskStatus.done.value and new_status == TaskStatus.in_progress.value:
            raise BusinessException("Cannot revert a done task to in_progress")

        
        task = self.repo.update_status(task, new_status)
        return task

    def delete_task(self, task_id):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise BusinessException("Task not found")
        if task.status == TaskStatus.in_progress.value:
            raise BusinessException("Cannot delete a task in progress")
        self.repo.delete(task)

    def get_overdue(self):
        return self.repo.overdue()
