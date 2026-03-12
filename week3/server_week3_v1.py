from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_PREFIX = "/api/v1"
tasks = {
    1: {"id": 1, "title": "Study SOA week 3", "done": False},
    2: {"id": 2, "title": "Prepare API versioning demo", "done": False},
}
next_id = 3


def task_representation(task):
    return {
        "id": task["id"],
        "title": task["title"],
        "done": task["done"],
        "links": {
            "self": url_for("get_task_v1", task_id=task["id"], _external=True),
            "collection": url_for("get_tasks_v1", _external=True),
        },
    }


@app.get("/")
def index():
    return jsonify(
        {
            "message": "SOA week 3 - version 1",
            "focus": "API versioning",
            "available_versions": ["v1"],
            "resources": {
                "tasks": f"{API_PREFIX}/tasks",
            },
        }
    )


@app.get(f"{API_PREFIX}/tasks")
def get_tasks_v1():
    items = [task_representation(task) for task in tasks.values()]
    return jsonify({"api_version": "v1", "items": items}), 200


@app.post(f"{API_PREFIX}/tasks")
def create_task_v1():
    global next_id

    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "'title' is required"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "done": bool(data.get("done", False)),
    }
    tasks[next_id] = task
    next_id += 1

    return jsonify(task_representation(task)), 201


@app.get(f"{API_PREFIX}/tasks/<int:task_id>")
def get_task_v1(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task_representation(task)), 200


if __name__ == "__main__":
    app.run(port=5001)
