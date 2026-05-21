import json
import os

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


def call(method, path, **kwargs):
    response = requests.request(method, f"{BASE_URL}{path}", timeout=5, **kwargs)
    if response.text:
        body = response.json()
    else:
        body = None
    return {"status": response.status_code, "body": body}


def step(title, func):
    print(f"\n=== {title} ===")
    result = func()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main():
    step("1. API index exposes HATEOAS links", lambda: call("GET", "/"))

    step(
        "2. Query users by active=true",
        lambda: call("GET", "/users?active=true&limit=5"),
    )

    created = step(
        "3. CRUD: create notification, then event-driven webhook runs",
        lambda: call(
            "POST",
            "/notifications",
            json={
                "userId": "u_1",
                "channel": "email",
                "message": "Don hang SOA-1001 da duoc xac nhan",
            },
        ),
    )

    notification_id = created["body"]["data"]["id"]

    step(
        "4. HATEOAS action: mark notification as read",
        lambda: call("POST", f"/notifications/{notification_id}/mark-read"),
    )

    step(
        "5. RPC-style: CountUnread is action-oriented",
        lambda: call(
            "POST",
            "/rpc",
            json={
                "method": "NotificationService.CountUnread",
                "params": {"userId": "u_1"},
            },
        ),
    )

    step(
        "6. GraphQL-style: client selects only needed fields",
        lambda: call(
            "POST",
            "/graphql",
            json={
                "fields": ["id", "message", "readAt"],
                "variables": {"userId": "u_1"},
            },
        ),
    )

    step("7. Webhook delivery log", lambda: call("GET", "/webhook-deliveries"))


if __name__ == "__main__":
    main()
