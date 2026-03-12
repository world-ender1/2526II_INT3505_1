from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_PREFIX = "/api/v1"
RESOURCE_NAME = "task-items"


task_items = {
    1: {"id": 1, "title": "Study SOA week 3", "done": False},
    2: {"id": 2, "title": "Make API responses easy to understand", "done": False},
}
next_id = 3


# CONSISTENCY (giữ từ v3): cùng response envelope cho mọi endpoint.
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
            "self": url_for("get_task_item_v4", task_item_id=task_item["id"], _external=True),
            "collection": url_for("get_task_items_v4", _external=True),
            "spec": url_for("get_task_items_spec_v4", _external=True),
        },
    }


# CLARITY: validate rõ từng field + trả hướng dẫn cụ thể.
def validate_create_payload(payload):
    if payload is None:
        return (
            "INVALID_JSON_BODY",
            "Request body must be valid JSON",
            {
                "expected_content_type": "application/json",
                "example": {"title": "Learn SOA", "done": False},
            },
        )

    if "title" not in payload:
        return (
            "TITLE_REQUIRED",
            "Field 'title' is required",
            {
                "field": "title",
                "expected_type": "string",
                "example": "Learn SOA",
            },
        )

    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        return (
            "TITLE_INVALID",
            "Field 'title' must be a non-empty string",
            {
                "field": "title",
                "expected_type": "string",
                "example": "Learn SOA",
            },
        )

    if "done" in payload and not isinstance(payload.get("done"), bool):
        return (
            "DONE_INVALID",
            "Field 'done' must be boolean if provided",
            {
                "field": "done",
                "expected_type": "boolean",
                "example": False,
            },
        )

    return None


@app.get("/")
def index_v4():
    return success_response(
        data={
            "focus": "Clarity",
            "clarity_rules": [
                "Field-level validation messages",
                "Actionable error details",
                "Self-descriptive endpoint specification",
            ],
            "resources": {RESOURCE_NAME: f"{API_PREFIX}/{RESOURCE_NAME}"},
            "spec_endpoint": f"{API_PREFIX}/{RESOURCE_NAME}/spec",
        },
        message="SOA week 3 - version 4",
    )


# CLARITY: endpoint mô tả contract để client hiểu nhanh cách gọi API.
@app.get(f"{API_PREFIX}/{RESOURCE_NAME}/spec")
def get_task_items_spec_v4():
    return success_response(
        data={
            "resource": RESOURCE_NAME,
            "create_request_example": {
                "title": "Learn SOA",
                "done": False,
            },
            "field_rules": {
                "title": "required, non-empty string",
                "done": "optional, boolean",
            },
            "possible_error_codes": [
                "INVALID_JSON_BODY",
                "TITLE_REQUIRED",
                "TITLE_INVALID",
                "DONE_INVALID",
                "TASK_ITEM_NOT_FOUND",
            ],
        },
        message="Task-items contract specification",
    )


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}")
def get_task_items_v4():
    items = [task_item_representation(task_item) for task_item in task_items.values()]
    return success_response(
        data=items,
        message="Task items fetched",
        meta={"count": len(items)},
    )


@app.post(f"{API_PREFIX}/{RESOURCE_NAME}")
def create_task_item_v4():
    global next_id

    payload = request.get_json(silent=True)
    validation_error = validate_create_payload(payload)
    if validation_error:
        error_code, message, details = validation_error
        return error_response(error_code=error_code, message=message, status_code=400, details=details)

    task_item = {
        "id": next_id,
        "title": payload["title"].strip(),
        "done": bool(payload.get("done", False)),
    }
    task_items[next_id] = task_item
    next_id += 1

    return success_response(
        data=task_item_representation(task_item),
        status_code=201,
        message="Task item created",
    )


@app.get(f"{API_PREFIX}/{RESOURCE_NAME}/<int:task_item_id>")
def get_task_item_v4(task_item_id):
    task_item = task_items.get(task_item_id)
    if not task_item:
        return error_response(
            error_code="TASK_ITEM_NOT_FOUND",
            message="Task item not found",
            status_code=404,
            details={
                "task_item_id": task_item_id,
                "hint": "Use GET /api/v1/task-items to list available ids",
            },
        )

    return success_response(
        data=task_item_representation(task_item),
        message="Task item fetched",
    )


if __name__ == "__main__":
    app.run(port=5004)
