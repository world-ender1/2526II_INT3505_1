from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_PREFIX = "/api/v1"


class InMemoryResourceService:
    def __init__(self, seed_items):
        self.items = {item["id"]: item for item in seed_items}
        self.next_id = (max(self.items.keys()) + 1) if self.items else 1

    def list_items(self):
        return [self.items[item_id] for item_id in sorted(self.items.keys())]

    def get_item(self, item_id):
        return self.items.get(item_id)

    def create_item(self, payload):
        item = {
            "id": self.next_id,
            "title": payload["title"].strip(),
            "done": bool(payload.get("done", False)),
        }
        self.items[self.next_id] = item
        self.next_id += 1
        return item


RESOURCES = {
    "task-items": {
        "service": InMemoryResourceService(
            [
                {"id": 1, "title": "Study SOA week 3", "done": False},
                {"id": 2, "title": "Design extensible API", "done": False},
            ]
        )
    },
    "note-items": {
        "service": InMemoryResourceService(
            [
                {"id": 1, "title": "Demo second resource without new handlers", "done": False}
            ]
        )
    },
}


def success_response(resource, data, status_code=200, message="Request processed successfully", meta=None):
    body = {
        "status": "success",
        "api_version": "v1",
        "resource": resource,
        "message": message,
        "data": data,
        "meta": meta or {},
    }
    return jsonify(body), status_code


def error_response(resource, error_code, message, status_code, details=None):
    body = {
        "status": "error",
        "api_version": "v1",
        "resource": resource,
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {},
        },
    }
    return jsonify(body), status_code


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
            },
        )

    if "done" in payload and not isinstance(payload.get("done"), bool):
        return (
            "DONE_INVALID",
            "Field 'done' must be boolean if provided",
            {
                "field": "done",
                "expected_type": "boolean",
            },
        )

    return None


def get_resource_config(resource):
    config = RESOURCES.get(resource)
    if not config:
        return None, error_response(
            resource=resource,
            error_code="RESOURCE_NOT_FOUND",
            message="Resource is not supported",
            status_code=404,
            details={"supported_resources": sorted(list(RESOURCES.keys()))},
        )
    return config, None


def item_representation(resource, item):
    return {
        "id": item["id"],
        "title": item["title"],
        "done": item["done"],
        "links": {
            "self": url_for("get_item", resource=resource, item_id=item["id"], _external=True),
            "collection": url_for("get_items", resource=resource, _external=True),
            "spec": url_for("get_resource_spec", resource=resource, _external=True),
        },
    }


@app.get("/")
def index_v5():
    return success_response(
        resource="api-root",
        data={
            "focus": "Extensibility",
            "extensibility_rule": "Add new resources by updating RESOURCES config only",
            "available_resources": sorted(list(RESOURCES.keys())),
            "collection_pattern": f"{API_PREFIX}/<resource>",
            "item_pattern": f"{API_PREFIX}/<resource>/<id>",
        },
        message="SOA week 3 - version 5",
    )


@app.get(f"{API_PREFIX}/<resource>/spec")
def get_resource_spec(resource):
    config, error = get_resource_config(resource)
    if error:
        return error

    return success_response(
        resource=resource,
        data={
            "resource": resource,
            "field_rules": {
                "title": "required, non-empty string",
                "done": "optional, boolean",
            },
            "create_request_example": {"title": "Learn SOA", "done": False},
            "endpoints": {
                "collection": f"{API_PREFIX}/{resource}",
                "item": f"{API_PREFIX}/{resource}/<id>",
            },
        },
        message="Resource contract specification",
        meta={"seed_count": len(config["service"].list_items())},
    )


@app.get(f"{API_PREFIX}/<resource>")
def get_items(resource):
    config, error = get_resource_config(resource)
    if error:
        return error

    items = [item_representation(resource, item) for item in config["service"].list_items()]
    return success_response(
        resource=resource,
        data=items,
        message="Items fetched",
        meta={"count": len(items)},
    )


@app.post(f"{API_PREFIX}/<resource>")
def create_item(resource):
    config, error = get_resource_config(resource)
    if error:
        return error

    payload = request.get_json(silent=True)
    validation_error = validate_create_payload(payload)
    if validation_error:
        error_code, message, details = validation_error
        return error_response(resource=resource, error_code=error_code, message=message, status_code=400, details=details)

    item = config["service"].create_item(payload)
    return success_response(
        resource=resource,
        data=item_representation(resource, item),
        status_code=201,
        message="Item created",
    )


@app.get(f"{API_PREFIX}/<resource>/<int:item_id>")
def get_item(resource, item_id):
    config, error = get_resource_config(resource)
    if error:
        return error

    item = config["service"].get_item(item_id)
    if not item:
        return error_response(
            resource=resource,
            error_code="ITEM_NOT_FOUND",
            message="Item not found",
            status_code=404,
            details={"item_id": item_id},
        )

    return success_response(
        resource=resource,
        data=item_representation(resource, item),
        message="Item fetched",
    )


if __name__ == "__main__":
    app.run(port=5005)
