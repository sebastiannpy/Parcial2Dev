from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService, BusinessException
from app.dto import TaskCreateDTO

tasks_bp = Blueprint('tasks', __name__)
service = TaskService()

@tasks_bp.route('', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        dto = TaskCreateDTO(**data)
        task = service.create_task(dto)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status
        }), 201
    except BusinessException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tasks_bp.route('', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    tasks = service.list_tasks(status)
    return jsonify([
        {"id": t.id, "title": t.title, "status": t.status, "due_date": str(t.due_date) if t.due_date else None}
        for t in tasks
    ])


@tasks_bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    try:
        data = request.get_json()
        new_status = data.get("status")

        if not new_status:
            return jsonify({"error": "Debe especificar el nuevo estado"}), 400

        task = service.update_status(task_id, new_status)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "status": task.status
        }), 200
    except BusinessException as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        service.delete_task(task_id)
        return '', 204
    except BusinessException as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route('/overdue', methods=['GET'])
def overdue_tasks():
    tasks = service.get_overdue()
    return jsonify([
        {"id": t.id, "title": t.title, "due_date": str(t.due_date)}
        for t in tasks
    ])
