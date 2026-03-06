from flask import Flask, jsonify, request, url_for
from pathlib import Path

app = Flask(__name__)

DB_FILE = Path(__file__).with_name("db.txt")
tasks = {}
next_id = 1


def str_to_bool(value):
    return str(value).strip().lower() == "true"


def load_tasks_from_file():
    global tasks, next_id

    loaded_tasks = {}
    if DB_FILE.exists():
        lines = DB_FILE.read_text(encoding="utf-8").splitlines()
        for line in lines:
            content = line.strip()
            if not content or content.startswith("#"):
                continue

            parts = content.split("|", 2)
            if len(parts) != 3:
                continue

            task_id_raw, title, done_raw = parts
            try:
                task_id = int(task_id_raw)
            except ValueError:
                continue

            loaded_tasks[task_id] = {
                "id": task_id,
                "title": title,
                "done": str_to_bool(done_raw),
            }

    tasks = loaded_tasks
    next_id = (max(tasks.keys()) + 1) if tasks else 1


def save_tasks_to_file():
    lines = ["# Simple text database", "# Format: id|title|done"]
    for task_id in sorted(tasks.keys()):
        task = tasks[task_id]
        lines.append(f"{task['id']}|{task['title']}|{task['done']}")
    DB_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


load_tasks_from_file()


def get_client_id():
    client_id = request.headers.get("X-Client-Id")
    if not client_id:
        return None
    return client_id


@app.before_request
def enforce_stateless_header():
    if request.path.startswith("/tasks") and not get_client_id():
        return jsonify({"error": "Thieu header X-Client-Id"}), 400


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
            "stateless": "Moi request can gui header X-Client-Id",
            "resources": {
                "tasks": url_for("get_tasks", _external=True),
            },
        }
    )


@app.get('/tasks')
def get_tasks():
    client_id = get_client_id()

    result = [task_representation(task) for task in tasks.values()]
    return jsonify({"client_id": client_id, "items": result}), 200


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
    save_tasks_to_file()

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
    save_tasks_to_file()
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

    save_tasks_to_file()

    return jsonify(task_representation(task)), 200


@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    save_tasks_to_file()
    return "", 204

if __name__ == '__main__':
    app.run(port=5000)