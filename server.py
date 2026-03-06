from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

tasks = {
    1: {"id": 1, "title": "Hoc REST", "done": False},
    2: {"id": 2, "title": "Lam demo uniform interface", "done": False},
}
next_id = 3


def task_representation(task):
    return {
        "id": task["id"],
        "title": task["title"],
        "done": task["done"],
        "links": {
            "self": url_for("get_task", task_id=task["id"], _external=True),
            "collection": url_for("get_tasks", _external=True),
        },
    }

@app.route('/')
def hello():
    return jsonify(
        {
            "message": "REST API dang chay",
            "resources": {
                "tasks": url_for("get_tasks", _external=True),
            },
        }
    )


@app.get('/tasks')
def get_tasks():
    result = [task_representation(task) for task in tasks.values()]
    return jsonify(result), 200


@app.post('/tasks')
def create_task():
    global next_id

    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "'title' la bat buoc"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "done": bool(data.get("done", False)),
    }
    tasks[next_id] = task
    next_id += 1

    return jsonify(task_representation(task)), 201


@app.get('/tasks/<int:task_id>')
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    return jsonify(task_representation(task)), 200


@app.put('/tasks/<int:task_id>')
def replace_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data or "done" not in data:
        return jsonify({"error": "Can day du 'title' va 'done' cho PUT"}), 400

    task["title"] = data["title"]
    task["done"] = bool(data["done"])
    return jsonify(task_representation(task)), 200


@app.patch('/tasks/<int:task_id>')
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON khong hop le"}), 400

    if "title" in data:
        task["title"] = data["title"]
    if "done" in data:
        task["done"] = bool(data["done"])

    return jsonify(task_representation(task)), 200


@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    return "", 204

if __name__ == '__main__':
    app.run(port=5000)