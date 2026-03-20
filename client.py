import requests

# ── Cấu hình ──────────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:5000"
HEADERS  = {"X-Client-Id": "client-A"}

# ── Cache local: lưu {url: {"etag": str, "data": dict}} ──────────────────────
_cache: dict = {}


def cached_get(url: str) -> tuple[int, dict | None]:
    """
    GET có cache:
      - Lần đầu: lấy data + lưu ETag vào _cache.
      - Lần sau: gửi If-None-Match; nếu server trả 304 → dùng data từ cache.
    Trả về (status_code, data).
    """
    req_headers = dict(HEADERS)
    if url in _cache:
        req_headers["If-None-Match"] = _cache[url]["etag"]
        print(f"  [Cache] Gui If-None-Match: {_cache[url]['etag'][:8]}…")
    else:
        print("  [Cache] Chua co cache, gui request binh thuong")

    resp = requests.get(url, headers=req_headers)

    if resp.status_code == 304:
        print("  [Cache] Server tra 304 Not Modified → dung data tu cache (tiet kiem bandwidth!)")
        return 304, _cache[url]["data"]

    # Cập nhật cache nếu server trả ETag
    etag = resp.headers.get("ETag")
    if etag:
        _cache[url] = {"etag": etag, "data": resp.json()}
        print(f"  [Cache] Luu ETag moi: {etag[:8]}…  Cache-Control: {resp.headers.get('Cache-Control')}")

    return resp.status_code, resp.json()


def separator(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)


try:
    # ── 1. Lần đầu GET /tasks → nhận data + lưu ETag ─────────────────────────
    separator("1. GET /tasks lan dau (chua co cache)")
    status, data = cached_get(f"{BASE_URL}/tasks")
    print(f"  Status: {status}  |  So task: {len(data['items'])}")

    # ── 2. GET /tasks lại → server trả 304 ───────────────────────────────────
    separator("2. GET /tasks lan 2 (data chua doi) → ky vong 304")
    status, data = cached_get(f"{BASE_URL}/tasks")
    print(f"  Status: {status}  |  Data tu cache: {[t['title'] for t in data['items']]}")

    # ── 3. Tạo task mới → dữ liệu thay đổi ──────────────────────────────────
    separator("3. POST /tasks (tao task moi → du lieu thay doi)")
    resp = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": "Demo Cacheable", "done": False},
        headers=HEADERS,
    )
    print(f"  Status: {resp.status_code}  |  Task moi: {resp.json()['title']}")

    # Xoá cache cũ vì biết dữ liệu đã thay đổi
    _cache.pop(f"{BASE_URL}/tasks", None)
    print("  [Cache] Da xoa cache /tasks (du lieu da thay doi)")

    # ── 4. GET /tasks lại → ETag mới, phải lấy data mới ──────────────────────
    separator("4. GET /tasks sau khi tao task → ky vong 200 voi ETag moi")
    status, data = cached_get(f"{BASE_URL}/tasks")
    print(f"  Status: {status}  |  So task hien tai: {len(data['items'])}")

    # ── 5. GET /tasks lần nữa → lại 304 (cache hợp lệ) ───────────────────────
    separator("5. GET /tasks lan nua (cache hop le) → ky vong 304")
    status, data = cached_get(f"{BASE_URL}/tasks")
    print(f"  Status: {status}  |  Dung cache: {[t['title'] for t in data['items']]}")

    # ── 6. GET task cụ thể ────────────────────────────────────────────────────
    separator("6. GET /tasks/1 lan dau va lan 2")
    status, task = cached_get(f"{BASE_URL}/tasks/1")
    print(f"  Lan 1 → Status: {status}  |  Task: {task['title']}")
    status, task = cached_get(f"{BASE_URL}/tasks/1")
    print(f"  Lan 2 → Status: {status}  |  (Tu cache) Task: {task['title']}")

    print("\n[DONE] Cacheable demo hoan tat!")

except requests.exceptions.ConnectionError:
    print("Khong the ket noi! Hay chac chan server Flask dang chay.")