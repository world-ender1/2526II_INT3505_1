import urllib.request
import urllib.error
import json

BASE_URL = "http://127.0.0.1:5000"

def make_request(method, path, data=None, token=None):
    url = BASE_URL + path
    headers = {}
    if data:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = f"Bearer {token}"
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

print("--- TEST MẬT MÃ BẢO VỆ (KHÔNG CÓ TOKEN) ---")
status, body = make_request('GET', '/tasks')
print(f"Status: {status} | Body: {body}")

print("\n--- TEST LOGIN VỚI VAI TRÒ ADMIN ---")
status, login_res = make_request('POST', '/auth/token', {'client_id': 'sv123', 'role': 'admin'})
print(f"Status: {status} | Access Token: {login_res.get('access_token')[:20]}... | Refresh Token: {login_res.get('refresh_token')[:20]}...")
access_token = login_res['access_token']
refresh_token = login_res['refresh_token']

print("\n--- DÙNG ACCESS TOKEN GỌI DATA ---")
status, tasks_res = make_request('GET', '/tasks', token=access_token)
print(f"Status: {status} | Tài khoản: {tasks_res.get('client_id')} | Quyền: {tasks_res.get('role')} | Số lượng task: {len(tasks_res.get('items', []))}")

print("\n--- DÙNG REFRESH TOKEN ĐỔI ACCESS TOKEN MỚI ---")
status, refresh_res = make_request('POST', '/auth/refresh', {'refresh_token': refresh_token})
print(f"Status: {status} | Access Token Xịn Mới: {refresh_res.get('access_token')[:20]}...")
