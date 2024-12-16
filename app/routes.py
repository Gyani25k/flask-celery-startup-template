from flask import Flask, jsonify, request
from app import create_app, db
from app.models import TaskResult
from app.tasks import background_task

app = create_app()

@app.before_request
def create_tables():
    db.create_all()

@app.route('/start-task', methods=['POST'])
def start_task():
    data = request.json
    print(data)
    user_input = data.get('input')

    # Trigger Celery Task
    task = background_task.apply_async(args=[user_input])
    return jsonify({"message": "Task started", "task_id": task.id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = background_task.AsyncResult(task_id)
    return jsonify({"state": task.state, "info": task.info})

@app.route('/results', methods=['GET'])
def get_results():
    tasks = TaskResult.query.all()
    results = [{"id": task.id, "input": task.input_data, "result": task.result, "status": task.status} for task in tasks]
    return jsonify(results)
