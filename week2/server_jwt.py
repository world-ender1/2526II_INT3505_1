import base64
import hashlib
import hmac
import json
import time
from pathlib import Path

from flask import Flask, g, jsonify, make_response, request, url_for

app = Flask(__name__)

DB_FILE = Path(__file__).with_name("db.txt")
JWT_SECRET = "soa-week2-secret-key"
JWT_ALG = "HS256"
JWT_EXPIRES_SECONDS = 3600

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


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64url_decode(raw: str) -> bytes:
    padding = "=" * ((4 - len(raw) % 4) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def create_jwt(payload: dict) -> str:
    header = {"alg": JWT_ALG, "typ": "JWT"}
    header_part = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_part = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_part}.{payload_part}".encode()
    signature = hmac.new(JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()
    signature_part = _b64url_encode(signature)
    return f"{header_part}.{payload_part}.{signature_part}"


def verify_jwt(token: str):
    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError:
        return None, "Token khong dung dinh dang JWT"

    signing_input = f"{header_part}.{payload_part}".encode()
    expected_signature = hmac.new(JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()

    try:
        provided_signature = _b64url_decode(signature_part)
    except Exception:
        return None, "Chu ky token khong hop le"

    if not hmac.compare_digest(provided_signature, expected_signature):
        return None, "Chu ky token khong hop le"

    try:
        payload = json.loads(_b64url_decode(payload_part).decode())
    except Exception:
        return None, "Payload token khong hop le"

    exp = payload.get("exp")
    if exp is None or not isinstance(exp, (int, float)):
        return None, "Token thieu exp"

    if time.time() > exp:
        return None, "Token da het han"

    return payload, None


def get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:].strip()


@app.before_request
def enforce_stateless_with_jwt():
    if request.path.startswith("/tasks"):
        token = get_bearer_token()
        if not token:
            return jsonify({"error": "Thieu Authorization: Bearer <token>"}), 401

        payload, error = verify_jwt(token)
        if error:
            return jsonify({"error": error}), 401

        g.client_id = payload.get("sub")


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


def compute_etag(data) -> str:
    serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(serialized.encode()).hexdigest()


def make_cached_response(body: dict, status: int = 200, max_age: int = 30):
    etag = compute_etag(body)
    client_etag = request.headers.get("If-None-Match")

    if client_etag == etag:
        resp = make_response("", 304)
        resp.headers["ETag"] = etag
        resp.headers["Cache-Control"] = f"max-age={max_age}"
        return resp

    resp = make_response(jsonify(body), status)
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = f"max-age={max_age}"
    return resp


@app.route("/")
def hello():
    return jsonify(
        {
            "message": "REST API dang chay",
            "stateless": "Moi request /tasks can gui Authorization: Bearer <JWT>",
            "auth": {
                "issue_token": url_for("issue_token", _external=True),
            },
            "resources": {
                "tasks": url_for("get_tasks", _external=True),
            },
        }
    )


@app.post("/auth/token")
def issue_token():
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")

    if not client_id:
        return jsonify({"error": "'client_id' la bat buoc"}), 400

    now = int(time.time())
    payload = {
        "sub": str(client_id),
        "iat": now,
        "exp": now + JWT_EXPIRES_SECONDS,
    }
    token = create_jwt(payload)

    return jsonify(
        {
            "token_type": "Bearer",
            "access_token": token,
            "expires_in": JWT_EXPIRES_SECONDS,
        }
    ), 200


@app.get("/tasks")
def get_tasks():
    result = [task_representation(task) for task in tasks.values()]
    body = {"client_id": g.get("client_id"), "items": result}
    return make_cached_response(body, status=200)


@app.post("/tasks")
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


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    return make_cached_response(task_representation(task), status=200)


@app.put("/tasks/<int:task_id>")
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


@app.patch("/tasks/<int:task_id>")
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


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    save_tasks_to_file()
    return "", 204


if __name__ == "__main__":
    app.run(port=5000)
