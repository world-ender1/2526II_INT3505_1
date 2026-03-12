import requests

BASE_URL = "http://127.0.0.1:5004"
API_PREFIX = "/api/v1"
RESOURCE_NAME = "task-items"


def print_result(label, response):
    print(f"\n{label}")
    print("Status:", response.status_code)
    print("Body:", response.json())


try:
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)

    response = requests.get(f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}/spec")
    print_result("GET /api/v1/task-items/spec", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}",
        json={"title": "  Clarity demo from client  ", "done": False},
    )
    print_result("POST /api/v1/task-items (valid)", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}",
        json={"done": False},
    )
    print_result("POST /api/v1/task-items (missing title)", response)

    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/{RESOURCE_NAME}",
        json={"title": "Invalid done type", "done": "false"},
    )
    print_result("POST /api/v1/task-items (done is string)", response)

except requests.exceptions.ConnectionError:
    print("Cannot connect. Run: python week3/server_week3_v4.py")
