from locust import HttpUser, task, between

class APIUser(HttpUser):
    # Thời gian chờ random giữa các request (1 đến 3 giây)
    wait_time = between(1, 3)

    @task(3) # Trọng số 3: Tần suất gọi endpoint này nhiều gấp 3 lần endpoint dưới
    def get_all_products(self):
        # Giả lập thao tác người dùng lấy danh sách sản phẩm
        self.client.get("/products", name="GET /products")

    @task(1)
    def get_single_product(self):
        self.client.get("/products/1", name="GET /products/[id]")

    @task(1)
    def create_product(self):
        self.client.post("/products", json={"name": "Load Test Item", "price": 99}, name="POST /products")
