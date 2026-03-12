import requests

BASE_URL = "http://127.0.0.1:5005"
API_PREFIX = "/api/v1"


def print_result(label, response):
    print(f"\n{label}")
    print("Status:", response.status_code)
    print("Body:", response.json())


try:
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/task-items")
    print_result("GET /api/v1/task-items", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/task-items",
        json={"title": "Created via generic handler", "done": False},
    )
    print_result("POST /api/v1/task-items", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/note-items")
    print_result("GET /api/v1/note-items (second resource)", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/note-items",
        json={"title": "New note item", "done": True},
    )
    print_result("POST /api/v1/note-items", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/unknown-items")
    print_result("GET /api/v1/unknown-items (unsupported resource)", response)

except requests.exceptions.ConnectionError:
    print("Cannot connect. Run: python week3/server_week3_v5.py")
