# Plan code demo Week 10: Service Operation - Security & Monitoring

## 1. Muc tieu demo

- Xay dung mot API service don gian bang Python/Flask.
- Tich hop logging de theo doi request, loi va hanh vi dang nhap.
- Expose metrics cho Prometheus qua endpoint `/metrics`.
- Ap dung rate limiting de bao ve API khoi spam/brute-force co ban.
- Chuan bi cau hinh deploy API len Vercel.

## 2. Cau truc project du kien

```text
w10/
+-- PLAN.md
+-- app.py
+-- requirements.txt
+-- vercel.json
`-- logs/
    `-- app.log
```

## 3. Cong nghe su dung

- Python 3.x
- Flask
- Flask-Limiter
- prometheus-flask-exporter
- Vercel Python Runtime
- Postman/curl de test API

## 4. Cac endpoint can demo

| Method | Endpoint | Muc dich |
| --- | --- | --- |
| `GET` | `/` | Kiem tra service dang chay |
| `GET` | `/api/status` | Tra ve trang thai he thong |
| `POST` | `/api/login` | Gia lap dang nhap va demo rate limiting |
| `GET` | `/metrics` | Expose metrics cho Prometheus |

## 5. Ke hoach code demo

### Buoc 1: Khoi tao Flask API

- Tao file `app.py`.
- Khoi tao Flask app.
- Tao route `/` va `/api/status`.
- Chay local bang lenh `python app.py`.
- Test nhanh bang `curl http://localhost:5001/api/status`.

### Buoc 2: Tich hop logging

- Su dung module `logging` co san cua Python.
- Cau hinh log format gom thoi gian, logger name, level va message.
- Ghi log ra console va file `logs/app.log`.
- Them log vao cac route: `INFO` khi API duoc goi, `WARNING` khi dang nhap that bai, `WARNING` khi bi rate limit.

### Buoc 3: Tich hop Prometheus metrics

- Cai `prometheus-flask-exporter`.
- Khoi tao `PrometheusMetrics(app)` trong `app.py`.
- Them metric thong tin app bang `metrics.info(...)`.
- Demo endpoint `/metrics` va giai thich request count, latency, status code.

### Buoc 4: Tich hop rate limiting

- Cai `Flask-Limiter`.
- Cau hinh global limit: `100 per 15 minutes`.
- Cau hinh endpoint `/api/login`: `5 per 15 minutes`.
- Goi `/api/login` nhieu lan de trigger HTTP `429 Too Many Requests`.

### Buoc 5: Chuan bi deploy Vercel

- Tao `requirements.txt` gom Flask, Flask-Limiter va prometheus-flask-exporter.
- Tao `vercel.json` dung runtime `@vercel/python`.
- Deploy bang Vercel CLI hoac GitHub Integration.
- Test lai endpoint bang domain Vercel duoc cap.

## 6. Checklist demo

- [ ] Cai dependencies tu `requirements.txt`.
- [ ] Chay Flask app local.
- [ ] Test `/api/status`.
- [ ] Kiem tra log tren console va file.
- [ ] Kiem tra `/metrics`.
- [ ] Trigger HTTP 429 tren `/api/login`.
- [ ] Trinh bay cau hinh deploy Vercel.

## 7. Mo rong

- Them audit log cho login.
- Tach config development/production.
- Them circuit breaker bang `pybreaker`.
- Gioi thieu WAF/API Gateway nhu Cloudflare, Kong hoac AWS API Gateway.
