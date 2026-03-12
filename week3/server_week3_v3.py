from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_PREFIX = "/api/v1"
RESOURCE_NAME = "task-items"


task_items = {
    1: {"id": 1, "title": "Study SOA week 3", "done": False},
    2: {"id": 2, "title": "Keep response format consistent", "done": False},
}
next_id = 3


# CONSISTENCY: mọi response thành công đều có cùng cấu trúc envelope.
def success_response(data, status_code=200, message="Request processed successfully", meta=None):
    body = {
        "status": "success",
        "api_version": "v1",
        "resource": RESOURCE_NAME,
        "message": message,
        "data": data,
        "meta": meta or {},
    }
    return jsonify(body), status_code


# CONSISTENCY: mọi response lỗi đều có cùng cấu trúc envelope.
def error_response(error_code, message, status_code, details=None):
    body = {
        "status": "error",
        "api_version": "v1",
        "resource": RESOURCE_NAME,
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {},
        },
    }
    return jsonify(body), status_code


def task_item_representation(task_item):
    return {
        "id": task_item["id"],
        "title": task_item["title"],
        "done": task_item["done"],
        "links": {
            "self": url_for("get_task_item_v3", task_item_id=task_item["id"], _external=True),
            "collection": url_for("get_task_items_v3", _external=True),
        },
    }


@app.get("/")
def index_v3():
    return success_response(
        data={
            "focus": "Consistency",
            "consistency_rule": "All endpoints return unified success/error envelope",
            "resources": {RESOURCE_NAME: f"{API_PREFIX}/{RESOURCE_NAME}"},
        },
        message="SOA week 3 - version 3",
    )


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}")
def get_task_items_v3():
    items = [task_item_representation(task_item) for task_item in task_items.values()]
    return success_response(
        data=items,
        message="Task items fetched",
        meta={"count": len(items)},
    )


@app.post(f"{API_PREFIX}/{RESOURCE_NAME}")
def create_task_item_v3():
    global next_id

    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return error_response(
            error_code="TITLE_REQUIRED",
            message="Field 'title' is required",
            status_code=400,
            details={"required_fields": ["title"]},
        )

    task_item = {
        "id": next_id,
        "title": data["title"],
        "done": bool(data.get("done", False)),
    }
    task_items[next_id] = task_item
    next_id += 1

    return success_response(
        data=task_item_representation(task_item),
        status_code=201,
        message="Task item created",
    )


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}/<int:task_item_id>")
def get_task_item_v3(task_item_id):
    task_item = task_items.get(task_item_id)
    if not task_item:
        return error_response(
            error_code="TASK_ITEM_NOT_FOUND",
            message="Task item not found",
            status_code=404,
            details={"task_item_id": task_item_id},
        )

    return success_response(
        data=task_item_representation(task_item),
        message="Task item fetched",
    )


if __name__ == "__main__":
    app.run(port=5003)
