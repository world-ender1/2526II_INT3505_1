from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_PREFIX = "/api/v1"
RESOURCE_NAME = "task-items"

task_items = {
    1: {"id": 1, "title": "Study SOA week 3", "done": False},
    2: {"id": 2, "title": "Apply naming conventions", "done": False},
}
next_id = 3


def task_item_representation(task_item):
    return {
        "id": task_item["id"],
        "title": task_item["title"],
        "done": task_item["done"],
        "links": {
            "self": url_for("get_task_item_v2", task_item_id=task_item["id"], _external=True),
            "collection": url_for("get_task_items_v2", _external=True),
        },
    }


@app.get("/")
def index():
    return jsonify(
        {
            "message": "SOA week 3 - version 2",
            "focus": "Naming conventions",
            "naming_conventions": [
                "plural nouns",
                "lowercase",
                "hyphens",
                "versioning",
            ],
            "resources": {
                RESOURCE_NAME: f"{API_PREFIX}/{RESOURCE_NAME}",
            },
        }
    )


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}")
def get_task_items_v2():
    items = [task_item_representation(task_item) for task_item in task_items.values()]
    return jsonify({"api_version": "v1", "resource": RESOURCE_NAME, "items": items}), 200


@app.post(f"{API_PREFIX}/{RESOURCE_NAME}")
def create_task_item_v2():
    global next_id

    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "'title' is required"}), 400

    task_item = {
        "id": next_id,
        "title": data["title"],
        "done": bool(data.get("done", False)),
    }
    task_items[next_id] = task_item
    next_id += 1

    return jsonify(task_item_representation(task_item)), 201


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}/<int:task_item_id>")
def get_task_item_v2(task_item_id):
    task_item = task_items.get(task_item_id)
    if not task_item:
        return jsonify({"error": "Task item not found"}), 404

    return jsonify(task_item_representation(task_item)), 200


if __name__ == "__main__":
    app.run(port=5002)
