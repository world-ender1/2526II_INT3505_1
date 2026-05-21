# Buoi 11-12: API Design Patterns

Thu muc nay gom ly thuyet ngan gon va demo code Flask cho cac mau thiet ke API:

- CRUD
- Query
- HATEOAS
- Event-driven
- Webhook
- Khi nao dung REST, gRPC/RPC, GraphQL
- Phan tich patterns trong Stripe va GitHub API

## Cach chay demo Flask

Mo terminal tai `D:\soa\week11_12`:

```bash
python -m pip install -r requirements.txt
python app.py
```

Mo terminal thu hai tai cung thu muc:

```bash
python demo_client.py
```

Server mac dinh chay tai:

```text
http://localhost:5000
```

Neu cong 5000 da duoc dung:

```powershell
$env:PORT=5001; python app.py
$env:BASE_URL="http://localhost:5001"; python demo_client.py
```

## 1. CRUD Pattern

CRUD la mau API cho thao tac co ban tren tai nguyen:

- Create: `POST /users`, `POST /notifications`
- Read: `GET /users`, `GET /users/<id>`
- Update: `PATCH /users/<id>`
- Delete: `DELETE /users/<id>`

Khi dung:

- Tai nguyen co vong doi ro rang.
- Client can tao, xem, sua, xoa entity.
- Phu hop voi REST.

Vi du:

```powershell
curl -X POST http://localhost:5000/users `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"Chi\",\"email\":\"chi@example.com\"}"
```

## 2. Query Pattern

Query pattern cho phep loc, tim kiem, phan trang, sap xep du lieu qua query string.

Trong demo:

```text
GET /users?active=true&q=an&page=1&limit=10
GET /notifications?userId=u_1&unreadOnly=true&page=1&limit=10
```

Khi dung:

- Danh sach co nhieu ban ghi.
- Client can filter/search/pagination.
- Query phai on dinh, de cache, de doc.

Luu y thiet ke:

- Dung ten query parameter ro nghia.
- Gioi han `limit` de tranh truy van qua nang.
- Tra ve metadata nhu `page`, `limit`, `total`, `totalPages`.

## 3. HATEOAS Pattern

HATEOAS la cach API tra ve link hanh dong lien quan ngay trong response. Client khong can hard-code tat ca URL.

Vi du response user trong demo co:

```json
{
  "id": "u_1",
  "name": "An",
  "_links": {
    "self": { "href": "/users/u_1", "method": "GET" },
    "update": { "href": "/users/u_1", "method": "PATCH" },
    "delete": { "href": "/users/u_1", "method": "DELETE" },
    "notifications": { "href": "/notifications?userId=u_1", "method": "GET" }
  }
}
```

Khi dung:

- API co workflow nhieu buoc.
- Client can biet hanh dong tiep theo hop le.
- Muon giam coupling giua client va URL noi bo.

## 4. Event-driven Pattern

Event-driven tach hanh dong chinh khoi xu ly phu bang event.

Trong demo:

1. Client goi `POST /notifications`.
2. Flask app tao notification.
3. Ham `emit_event("notification.created", notification)` phat event noi bo.
4. `dispatch_webhooks` nhan event va gui webhook cho subscriber.

Loi ich:

- Giam coupling giua module.
- De them xu ly moi ma khong sua flow chinh.
- Hop voi notification, audit log, email, payment, integration.

Can luu y:

- Event co the bi xu ly lai, nen consumer nen idempotent.
- Nen co log delivery, retry, dead-letter queue trong he thong that.
- Khong nen de user-facing request cho doi qua nhieu viec cham.

## 5. Webhook Pattern

Webhook la HTTP callback: he thong A goi sang he thong B khi co su kien.

Trong demo:

- Dang ky webhook: `POST /webhook-subscriptions`
- Receiver gia lap: `POST /demo/webhook-receiver`
- Log delivery: `GET /webhook-deliveries`

Webhook payload co dang:

```json
{
  "id": "evt_xxx",
  "type": "notification.created",
  "createdAt": "2026-05-21T00:00:00.000Z",
  "data": {
    "id": "noti_xxx",
    "message": "..."
  }
}
```

Demo co ky HMAC bang header `X-Webhook-Signature`.

Checklist webhook trong thuc te:

- Xac thuc chu ky HMAC.
- Retry khi receiver tra ve loi.
- Idempotency theo `event.id`.
- Luu delivery log.
- Cho phep subscriber chon event types.
- Khong gui secret/token trong payload.

## 6. Khi nao dung REST, gRPC/RPC, GraphQL

### REST

Dung REST khi:

- API xoay quanh tai nguyen nhu user, order, product.
- Can de debug bang browser/curl.
- Can cache, HTTP status code, HTTP method ro rang.
- Public API cho nhieu loai client.

Trong demo:

```text
GET /users
POST /notifications
PATCH /users/<id>
```

### gRPC/RPC

Dung gRPC hoac RPC-style khi:

- He thong noi bo service-to-service.
- Can performance cao, schema chat, streaming.
- Tac vu la hanh dong/dich vu hon la tai nguyen.

Trong demo co endpoint RPC-style:

```text
POST /rpc
```

Body:

```json
{
  "method": "NotificationService.CountUnread",
  "params": { "userId": "u_1" }
}
```

### GraphQL

Dung GraphQL khi:

- Client can lay nhieu loai du lieu trong mot request.
- Mobile/web can chon dung field can dung.
- Muon tranh over-fetching/under-fetching.

Trong demo co endpoint GraphQL-style:

```text
POST /graphql
```

Body:

```json
{
  "fields": ["id", "message", "readAt"],
  "variables": { "userId": "u_1" }
}
```

Ghi chu: Day la GraphQL-style demo de minh hoa field selection, khong phai GraphQL server day du.

## 7. Thiet ke API ket hop nhieu patterns

Mot API tot thuong khong chi dung mot pattern:

- REST CRUD cho tai nguyen chinh.
- Query cho danh sach.
- HATEOAS cho link va workflow.
- Event-driven de xu ly bat dong bo.
- Webhook de tich hop he thong ngoai.
- RPC/gRPC cho tac vu noi bo can goi nhu service method.
- GraphQL cho client can tu chon field va gom du lieu.

Demo notification system ket hop:

```text
POST /notifications
  -> tao notification
  -> emit notification.created
  -> webhook dispatcher gui event
  -> webhook receiver xac thuc chu ky
  -> webhook-deliveries luu ket qua
```

## 8. Phan tich Stripe API

Stripe API la vi du tot ve REST + event-driven + webhook:

- Dung resource ro rang: `customers`, `payment_intents`, `charges`, `subscriptions`.
- Dung CRUD/action endpoints: tao payment intent, confirm payment intent.
- Dung idempotency key de tranh tao trung giao dich khi retry.
- Dung webhook de thong bao su kien bat dong bo nhu thanh toan thanh cong, thanh toan that bai, subscription updated.
- Dung event object co `id`, `type`, `data` de consumer xu ly theo loai su kien.

Pattern nhin thay:

- REST resource API cho thao tac truc tiep.
- Webhook cho ket qua bat dong bo.
- Event-driven cho payment lifecycle.
- Query/list API cho phan trang va loc.

## 9. Phan tich GitHub API

GitHub API ket hop REST, GraphQL va webhook:

- REST API cho repo, issue, pull request, release.
- Query parameters cho list/filter/sort.
- Link/header pagination giup client duyet danh sach lon.
- GraphQL API cho truy van linh hoat, vi du lay repo, issue, PR, review trong mot request.
- Webhook cho event nhu `push`, `pull_request`, `issues`, `workflow_run`.

Pattern nhin thay:

- REST cho thao tac pho bien, de tich hop.
- GraphQL cho client can lay du lieu co cau truc rieng.
- Webhook cho automation va CI/CD.
- Event-driven vi moi hanh dong trong repo co the tao event.

## 10. Cau truc code

```text
week11_12/
  app.py
  demo_client.py
  requirements.txt
  README.md
```

Trong `app.py`:

- `list_users`, `create_user`, `update_user`, `delete_user`: CRUD + Query + HATEOAS cho users.
- `create_notification`, `mark_notification_read`: notification workflow.
- `emit_event`, `dispatch_webhooks`: event-driven dispatcher.
- `list_webhook_subscriptions`, `create_webhook_subscription`: webhook subscriptions.
- `demo_webhook_receiver`: receiver demo co verify signature.
- `rpc`: RPC-style endpoint.
- `graphql_style`: GraphQL-style field selection.

## 11. Bai tap mo rong

Ban co the tu lam them:

- Them retry webhook khi delivery failed.
- Them idempotency key cho `POST /notifications`.
- Them `sort=createdAt:desc` cho query notifications.
- Luu database ra file JSON.
- Viet test tu dong cho cac endpoint.
