import requests

# Địa chỉ của server Flask (mặc định là port 5000)
base_url = "http://127.0.0.1:5000"
headers = {"X-Client-Id": "client-A"}

try:
    print("GET /tasks (stateless: gui X-Client-Id trong moi request)")
    response = requests.get(f"{base_url}/tasks", headers=headers)
    print(response.status_code, response.json())

except requests.exceptions.ConnectionError:
    print("Không thể kết nối! Hãy chắc chắn server Flask đang chạy.")