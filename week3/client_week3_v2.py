import requests

BASE_URL = "http://127.0.0.1:5002"
API_PREFIX = "/api/v1"
RESOURCE_NAME = "task-items"


def print_result(label, response):
    print(f"\n{label}")
    print("Status:", response.status_code)
    print("Body:", response.json())


try:
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}")
    print_result("GET /api/v1/task-items", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}",
        json={"title": "Resource name uses hyphen", "done": False},
    )
    print_result("POST /api/v1/task-items", response)

    task_item_id = response.json()["id"]
    response = requests.get(f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}/{task_item_id}")
    print_result(f"GET /api/v1/task-items/{task_item_id}", response)

except requests.exceptions.ConnectionError:
    print("Cannot connect. Run: python week3/server_week3_v2.py")
