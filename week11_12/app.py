from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timezone
from typing import Any

import requests
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

PORT = int(os.getenv("PORT", "5000"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "week11_12_secret")

db: dict[str, list[dict[str, Any]]] = {
    "users": [
        {"id": "u_1", "name": "An", "email": "an@example.com", "active": True},
        {"id": "u_2", "name": "Binh", "email": "binh@example.com", "active": True},
    ],
    "subscriptions": [
        {
            "id": "sub_1",
            "targetUrl": f"http://localhost:{PORT}/demo/webhook-receiver",
            "eventTypes": ["notification.created"],
            "active": True,
        }
    ],
    "notifications": [],
    "webhookDeliveries": [],
}


def new_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(4)}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_link(href: str, method: str = "GET") -> dict[str, str]:
    return {"href": href, "method": method}


def sign_payload(payload: bytes) -> str:
    return hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, signature: str | None) -> bool:
    if not signature:
        return False
    return hmac.compare_digest(sign_payload(payload), signature)


def paginate(items: list[dict[str, Any]]) -> dict[str, Any]:
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 10)), 1), 50)
    start = (page - 1) * limit
    total_pages = max((len(items) + limit - 1) // limit, 1)
    return {
        "page": page,
        "limit": limit,
        "total": len(items),
        "totalPages": total_pages,
        "data": items[start : start + limit],
    }


def user_resource(user: dict[str, Any]) -> dict[str, Any]:
    return {
        **user,
        "_links": {
            "self": make_link(f"/users/{user['id']}"),
            "update": make_link(f"/users/{user['id']}", "PATCH"),
            "delete": make_link(f"/users/{user['id']}", "DELETE"),
            "notifications": make_link(f"/notifications?userId={user['id']}"),
        },
    }


def notification_resource(notification: dict[str, Any]) -> dict[str, Any]:
    return {
        **notification,
        "_links": {
            "self": make_link(f"/notifications/{notification['id']}"),
            "user": make_link(f"/users/{notification['userId']}"),
            "markRead": make_link(f"/notifications/{notification['id']}/mark-read", "POST"),
        },
    }


def find_by_id(collection: str, item_id: str) -> dict[str, Any] | None:
    return next((item for item in db[collection] if item["id"] == item_id), None)


def emit_event(event_type: str, data: dict[str, Any]) -> None:
    if event_type == "notification.created":
        dispatch_webhooks(event_type, notification_resource(data))


def dispatch_webhooks(event_type: str, data: dict[str, Any]) -> None:
    event = {
        "id": new_id("evt"),
        "type": event_type,
        "createdAt": now_iso(),
        "data": data,
    }

    subscribers = [
        sub
        for sub in db["subscriptions"]
        if sub["active"] and event_type in sub["eventTypes"]
    ]

    for subscriber in subscribers:
        payload = json.dumps(event, separators=(",", ":")).encode()
        delivery = {
            "id": new_id("del"),
            "eventId": event["id"],
            "subscriptionId": subscriber["id"],
            "targetUrl": subscriber["targetUrl"],
            "status": "pending",
            "attemptedAt": now_iso(),
        }
        db["webhookDeliveries"].append(delivery)

        try:
            response = requests.post(
                subscriber["targetUrl"],
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Webhook-Event": event_type,
                    "X-Webhook-Signature": sign_payload(payload),
                },
                timeout=3,
            )
            delivery["status"] = "success" if 200 <= response.status_code < 300 else "failed"
            delivery["responseStatus"] = response.status_code
        except requests.RequestException as exc:
            delivery["status"] = "failed"
            delivery["error"] = str(exc)


@app.get("/")
def index() -> Response:
    return jsonify(
        {
            "title": "Week 11-12 API Design Patterns Demo",
            "patterns": [
                "CRUD",
                "Query",
                "HATEOAS",
                "Event-driven",
                "Webhook",
                "RPC-style",
                "GraphQL-style",
            ],
            "_links": {
                "users": make_link("/users"),
                "notifications": make_link("/notifications"),
                "webhookSubscriptions": make_link("/webhook-subscriptions"),
                "webhookDeliveries": make_link("/webhook-deliveries"),
                "rpc": make_link("/rpc", "POST"),
                "graphqlStyle": make_link("/graphql", "POST"),
            },
        }
    )


@app.get("/users")
def list_users() -> Response:
    users = list(db["users"])
    active = request.args.get("active")
    q = request.args.get("q", "").lower()

    if active is not None:
        users = [user for user in users if str(user["active"]).lower() == active.lower()]
    if q:
        users = [
            user
            for user in users
            if q in user["name"].lower() or q in user["email"].lower()
        ]

    return jsonify(
        {
            "pattern": "Query + HATEOAS",
            **paginate([user_resource(user) for user in users]),
            "_links": {
                "self": make_link(f"/users?{request.query_string.decode()}"),
                "create": make_link("/users", "POST"),
            },
        }
    )


@app.post("/users")
def create_user() -> tuple[Response, int, dict[str, str]] | tuple[Response, int]:
    body = request.get_json(silent=True) or {}
    if not body.get("name") or not body.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    user = {
        "id": new_id("u"),
        "name": body["name"],
        "email": body["email"],
        "active": body.get("active", True),
    }
    db["users"].append(user)
    return jsonify(user_resource(user)), 201, {"Location": f"/users/{user['id']}"}


@app.get("/users/<user_id>")
def get_user(user_id: str) -> Response | tuple[Response, int]:
    user = find_by_id("users", user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_resource(user))


@app.patch("/users/<user_id>")
def update_user(user_id: str) -> Response | tuple[Response, int]:
    user = find_by_id("users", user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    body = request.get_json(silent=True) or {}
    user["name"] = body.get("name", user["name"])
    user["email"] = body.get("email", user["email"])
    user["active"] = body.get("active", user["active"])
    return jsonify(user_resource(user))


@app.delete("/users/<user_id>")
def delete_user(user_id: str) -> tuple[str, int] | tuple[Response, int]:
    user = find_by_id("users", user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db["users"] = [item for item in db["users"] if item["id"] != user_id]
    return "", 204


@app.get("/notifications")
def list_notifications() -> Response:
    notifications = list(db["notifications"])
    user_id = request.args.get("userId")
    unread_only = request.args.get("unreadOnly")

    if user_id:
        notifications = [item for item in notifications if item["userId"] == user_id]
    if unread_only == "true":
        notifications = [item for item in notifications if not item["readAt"]]

    return jsonify(
        {
            "pattern": "Query + HATEOAS",
            **paginate([notification_resource(item) for item in notifications]),
            "_links": {
                "self": make_link(f"/notifications?{request.query_string.decode()}"),
                "create": make_link("/notifications", "POST"),
            },
        }
    )


@app.post("/notifications")
def create_notification() -> tuple[Response, int]:
    body = request.get_json(silent=True) or {}
    user = find_by_id("users", body.get("userId", ""))
    if not user:
        return jsonify({"error": "Valid userId is required"}), 400
    if not body.get("message"):
        return jsonify({"error": "message is required"}), 400

    notification = {
        "id": new_id("noti"),
        "userId": body["userId"],
        "channel": body.get("channel", "email"),
        "message": body["message"],
        "readAt": None,
        "createdAt": now_iso(),
    }
    db["notifications"].append(notification)
    emit_event("notification.created", notification)

    return (
        jsonify(
            {
                "pattern": "CRUD command triggers Event-driven workflow and Webhook delivery",
                "data": notification_resource(notification),
            }
        ),
        202,
    )


@app.get("/notifications/<notification_id>")
def get_notification(notification_id: str) -> Response | tuple[Response, int]:
    notification = find_by_id("notifications", notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify(notification_resource(notification))


@app.post("/notifications/<notification_id>/mark-read")
def mark_notification_read(notification_id: str) -> Response | tuple[Response, int]:
    notification = find_by_id("notifications", notification_id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    notification["readAt"] = now_iso()
    return jsonify(notification_resource(notification))


@app.get("/webhook-subscriptions")
def list_webhook_subscriptions() -> Response:
    return jsonify(
        {
            "pattern": "Webhook subscription management",
            "data": db["subscriptions"],
            "_links": {
                "self": make_link("/webhook-subscriptions"),
                "create": make_link("/webhook-subscriptions", "POST"),
                "deliveries": make_link("/webhook-deliveries"),
            },
        }
    )


@app.post("/webhook-subscriptions")
def create_webhook_subscription() -> tuple[Response, int, dict[str, str]] | tuple[Response, int]:
    body = request.get_json(silent=True) or {}
    if not body.get("targetUrl"):
        return jsonify({"error": "targetUrl is required"}), 400

    subscription = {
        "id": new_id("sub"),
        "targetUrl": body["targetUrl"],
        "eventTypes": body.get("eventTypes", ["notification.created"]),
        "active": body.get("active", True),
    }
    db["subscriptions"].append(subscription)
    return jsonify(subscription), 201, {"Location": f"/webhook-subscriptions/{subscription['id']}"}


@app.get("/webhook-deliveries")
def list_webhook_deliveries() -> Response:
    return jsonify(
        {
            "pattern": "Webhook delivery log for observability and retry design",
            "data": db["webhookDeliveries"],
        }
    )


@app.post("/demo/webhook-receiver")
def demo_webhook_receiver() -> tuple[Response, int] | Response:
    payload = request.get_data()
    signature = request.headers.get("X-Webhook-Signature")

    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid webhook signature"}), 401

    event = json.loads(payload)
    app.logger.info("webhook receiver accepted %s event %s", event["type"], event["id"])
    return jsonify(
        {
            "received": True,
            "eventType": event["type"],
            "message": "Webhook receiver verified signature and accepted event",
        }
    )


@app.post("/rpc")
def rpc() -> Response | tuple[Response, int]:
    body = request.get_json(silent=True) or {}
    if body.get("method") == "NotificationService.CountUnread":
        user_id = (body.get("params") or {}).get("userId")
        count = len(
            [
                item
                for item in db["notifications"]
                if item["userId"] == user_id and not item["readAt"]
            ]
        )
        return jsonify(
            {
                "pattern": "RPC-style endpoint for action-oriented service method",
                "result": {"unreadCount": count},
            }
        )

    return jsonify({"error": "Unknown RPC method"}), 404


@app.post("/graphql")
def graphql_style() -> Response:
    body = request.get_json(silent=True) or {}
    fields = body.get("fields", ["id", "message", "createdAt"])
    user_id = (body.get("variables") or {}).get("userId")

    notifications = [
        item for item in db["notifications"] if not user_id or item["userId"] == user_id
    ]
    selected = [
        {field: item.get(field) for field in fields}
        for item in notifications
    ]

    return jsonify(
        {
            "pattern": "GraphQL-style field selection demo",
            "data": {"notifications": selected},
        }
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=PORT, debug=debug)
