import json
import time
import uuid
import os
from pathlib import Path
from dotenv import load_dotenv

import jwt  # Dùng PyJWT chuẩn quốc tế thay vì tự viết
from flask import Flask, g, jsonify, make_response, request, url_for

# Load Secret từ file .env (Chống rò rỉ Key)
load_dotenv()

app = Flask(__name__)

DB_FILE = Path(__file__).with_name("db.txt")
# Trích xuất Secret từ biến môi trường. Nếu không có sẽ báo lỗi (Fail-fast)
JWT_SECRET = os.getenv("JWT_SECRET") 
if not JWT_SECRET:
    raise ValueError("Chưa thiết lập JWT_SECRET trong file .env!")

JWT_ALG = "HS256"
# Rút ngắn thời gian Access Token lại để giảm thiểu Replay Attack
ACCESS_TOKEN_EXPIRES_SECONDS = 15 * 60  # 15 phút
REFRESH_TOKEN_EXPIRES_SECONDS = 7 * 24 * 3600  # 7 ngày

tasks = {}
next_id = 1
# Mô phỏng một Blacklist (cho JTI - Token thu hồi) trong DB ảo
revoked_jtis = set()

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


# ==========================================================
# BẢO MẬT: THUẬT TOÁN JWT ĐÃ ĐƯỢC CHUYỂN QUA SỬ DỤNG THƯ VIỆN CHUẨN
# ==========================================================
def create_jwt(payload: dict) -> str:
    """Tạo JWT Token sử dụng PyJWT"""
    # Gắn thêm JTI (JWT ID) để chống Replay Attack nếu cần chặn đích danh 1 token
    if "jti" not in payload:
        payload["jti"] = str(uuid.uuid4())
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def verify_jwt(token: str):
    """Xác thực JWT Token sử dụng PyJWT"""
    try:
        # PyJWT dã tự động lo việc kiểm tra cấu trúc, Signature, và Hạn sử dụng (exp)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        
        # Kiểm tra xem JTI này có bị nằm trong sổ đen (Blacklist/Revoked) không
        if payload.get("jti") in revoked_jtis:
            return None, "Token nay da bi thu hoi (Revoked)"
            
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token da het han"
    except jwt.InvalidTokenError as e:
        return None, f"Token khong hop le: {str(e)}"


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
            
        # Kiểm tra Scope (Ví dụ API xóa cần quyền 'write' hoặc role 'admin')
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            scopes = payload.get("scopes", [])
            if "write" not in scopes and payload.get("role") != "admin":
                return jsonify({"error": "Token khong co quyen (scope) ghi du lieu"}), 403

        g.client_id = payload.get("sub")
        g.role = payload.get("role")


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

# ==========================================================
# CÁC ROUTE PHỤC VỤ AUTHENTICATION
# ==========================================================
@app.route("/")
def hello():
    return jsonify(
        {
            "message": "REST API dang chay (Secured)",
            "auth": {
                "issue_token": url_for("issue_token", _external=True),
                "refresh_token": url_for("refresh_token_api", _external=True),
            },
            "resources": {
                "tasks": url_for("get_tasks", _external=True),
            },
        }
    )


@app.post("/auth/token")
def issue_token():
    # Mô phỏng Login
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")

    if not client_id:
        return jsonify({"error": "'client_id' la bat buoc"}), 400

    now = int(time.time())
    
    # 1. Access Token Payload (Hạn ngắn - Có Scope và Role)
    access_payload = {
        "sub": str(client_id),
        "type": "access",
        "role": data.get("role", "user"), # Demo gán Role
        "scopes": ["read", "write"] if data.get("role") == "admin" else ["read"],
        "iat": now,
        "exp": now + ACCESS_TOKEN_EXPIRES_SECONDS,
        "jti": str(uuid.uuid4())
    }
    access_token = create_jwt(access_payload)
    
    # 2. Refresh Token Payload (Hạn dài - Không chứa Scope/Role để dỡ lộ)
    refresh_payload = {
        "sub": str(client_id),
        "type": "refresh",
        "iat": now,
        "exp": now + REFRESH_TOKEN_EXPIRES_SECONDS,
        "jti": str(uuid.uuid4())
    }
    refresh_token = create_jwt(refresh_payload)

    return jsonify(
        {
            "token_type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": ACCESS_TOKEN_EXPIRES_SECONDS,
        }
    ), 200


@app.post("/auth/refresh")
def refresh_token_api():
    """Route sử dụng Refresh Token để lấy lại Access Token mới"""
    data = request.get_json(silent=True) or {}
    req_refresh_token = data.get("refresh_token")
    
    if not req_refresh_token:
        return jsonify({"error": "Thieu refresh_token"}), 400
        
    payload, err = verify_jwt(req_refresh_token)
    if err:
        return jsonify({"error": "Refresh Token khong hop le hoac da han"}), 401
        
    if payload.get("type") != "refresh":
        return jsonify({"error": "Token truyen vao khong phai la Refresh Token"}), 400
        
    client_id = payload.get("sub")
    
    # Ở hệ thống thật: Cần check DB xem client_id bị ban chưa, hoặc refresh_token này bị thu hồi chưa.
    # Trong demo, sinh luôn Access Token mới (15 phút)
    now = int(time.time())
    new_access_payload = {
        "sub": str(client_id),
        "type": "access",
        "role": "user", # Fake role for demo
        "scopes": ["read"],
        "iat": now,
        "exp": now + ACCESS_TOKEN_EXPIRES_SECONDS,
        "jti": str(uuid.uuid4()) # ID mới chống Replay Attack
    }
    new_access_token = create_jwt(new_access_payload)
    
    return jsonify({
        "access_token": new_access_token,
        "expires_in": ACCESS_TOKEN_EXPIRES_SECONDS
    }), 200

# ==========================================================
# CÁC ROUTE PHỤC VỤ RESOURCE TASKS (Y HỆT CŨ)
# ==========================================================

@app.get("/tasks")
def get_tasks():
    result = [task_representation(task) for task in tasks.values()]
    return jsonify({"client_id": g.get("client_id"), "role": getattr(g, 'role', 'N/A'), "items": result}), 200

@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "'title' la bat buoc"}), 400
    task = {"id": next_id, "title": data["title"], "done": bool(data.get("done", False))}
    tasks[next_id] = task
    next_id += 1
    save_tasks_to_file()
    return jsonify(task_representation(task)), 201

@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    return jsonify(task_representation(task)), 200

@app.put("/tasks/<int:task_id>")
def replace_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Khong tim thay task"}), 404
    data = request.get_json(silent=True)
    if not data or "title" not in data or "done" not in data:
        return jsonify({"error": "Can day du 'title' va 'done'"}), 400
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
    if "title" in data: task["title"] = data["title"]
    if "done" in data: task["done"] = bool(data["done"])
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
