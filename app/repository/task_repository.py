from app.models import Task
from app.database import db
from datetime import date

class TaskRepository:
    def create(self, title, description, due_date):
        task = Task(title=title, description=description, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        return task

    def list(self, status=None):
        query = Task.query
        if status:
            query = query.filter_by(status=status)
        return query.all()

    def get_by_id(self, task_id):
        return Task.query.get(task_id)

    def update_status(self, task, new_status):
        task.status = new_status
        db.session.commit()
        return task

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()

    def overdue(self):
        today = date.today()
        return Task.query.filter(Task.due_date != None, Task.due_date < today).all()
