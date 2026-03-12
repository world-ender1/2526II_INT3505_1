import requests

BASE_URL = "http://127.0.0.1:5001"
API_PREFIX = "/api/v1"


def print_result(label, response):
    print(f"\n{label}")
    print("Status:", response.status_code)
    print("Body:", response.json())


try:
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/tasks")
    print_result("GET /api/v1/tasks", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/tasks",
        json={"title": "Versioning works", "done": False},
    )
    print_result("POST /api/v1/tasks", response)

    task_id = response.json()["id"]
    response = requests.get(f"{BASE_URL}{API_PREFIX}/tasks/{task_id}")
    print_result(f"GET /api/v1/tasks/{task_id}", response)

except requests.exceptions.ConnectionError:
    print("Cannot connect. Run: python server_week3_v1.py")
