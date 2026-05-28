# Plan Week 13: API as a Product

## 1. Muc tieu tuan 13

- Hieu API nhu mot san pham, khong chi la mot endpoint ky thuat.
- Biet cac thanh phan chinh cua API product: developer experience, monetization, analytics.
- Xac dinh KPI de do suc khoe va gia tri kinh doanh cua API.
- Thiet ke chien luoc ra mat API voi developer portal, documentation va sandbox.
- De xuat mo hinh kiem tien phu hop cho API cua nhom.
- Xay dung business model canvas va thiet ke developer portal don gian.

## 2. Kien thuc can dat

### API la san pham

API can duoc thiet ke nhu mot san pham danh cho developer:

- Developer experience: API de hieu, de dang ky, de test, de debug va de tich hop.
- Documentation: co quickstart, authentication, endpoint reference, example request/response va error guide.
- Sandbox: moi truong thu nghiem an toan, khong anh huong du lieu that.
- Support: co FAQ, contact, changelog va trang status.
- Trust: co versioning, rate limit ro rang, security policy va SLA co ban.

### Monetization

Mot API co the kiem tien bang nhieu mo hinh:

- Freemium: mien phi gioi han call volume, tinh phi khi vuot quota.
- Pay-per-call: tinh tien theo so request thanh cong.
- Subscription: goi thang/quy/nam theo quota va tinh nang.
- Tiered pricing: Free, Pro, Business, Enterprise.
- Revenue share: chia doanh thu voi doi tac tich hop API.

### Analytics

Can theo doi hanh vi developer va chat luong API:

- Developer signup: so developer/to chuc dang ky.
- Activation: so developer tao API key va goi thanh cong request dau tien.
- Call volume: tong so request theo ngay/tuan/thang.
- Error rate: ti le loi 4xx/5xx.
- Latency: thoi gian phan hoi trung binh va p95.
- Retention: developer con goi API sau 7 ngay/30 ngay.
- Conversion: ti le user tu free chuyen sang paid.

## 3. KPI can theo doi

| KPI | Y nghia | Cach do |
| --- | --- | --- |
| Developer signups | Do suc hut cua API | So tai khoan developer dang ky moi |
| API key created | Do muc do bat dau tich hop | So API key duoc tao |
| First successful call | Do activation | So developer goi API thanh cong lan dau |
| Call volume | Do muc do su dung | Tong request theo endpoint va theo ngay |
| Error rate | Do do on dinh | `(4xx + 5xx) / total requests` |
| Latency p95 | Do trai nghiem tich hop | 95% request nhanh hon moc thoi gian nay |
| Free-to-paid conversion | Do kha nang kiem tien | Paid developer / active free developer |

## 4. San pham thuc hanh can hoan thanh

- Business model canvas cho API nhom dang lam.
- Chien luoc ra mat API.
- De xuat mo hinh kiem tien.
- Thiet ke developer portal don gian.
- Checklist KPI va analytics dashboard can co.

## 5. Business model canvas cho API cua nhom

> Gia dinh API cua nhom la API quan ly sach/thu vien hoac API quan ly tai nguyen hoc tap. Neu nhom dang lam API khac, thay doi ten resource cho phu hop.

| Thanh phan | Noi dung de xuat |
| --- | --- |
| Customer Segments | Developer, truong hoc, thu vien, ung dung quan ly sach, ung dung hoc tap |
| Value Propositions | Cung cap API de quan ly sach, nguoi dung, muon/tra, tim kiem va thong ke nhanh |
| Channels | Developer portal, GitHub README, Postman collection, demo sandbox |
| Customer Relationships | Self-service docs, FAQ, email support, changelog |
| Revenue Streams | Freemium, pay-per-call, subscription theo quota, enterprise plan |
| Key Resources | API service, database, docs, sandbox, analytics, API gateway |
| Key Activities | Duy tri API, cap nhat docs, monitor loi, ho tro developer, toi uu performance |
| Key Partners | Truong hoc, thu vien, nha phat trien ung dung, payment provider |
| Cost Structure | Hosting, database, logging/monitoring, support, bao mat, phat trien tinh nang |

## 6. Chien luoc ra mat API

### Giai doan 1: Chuan bi API

- Chot danh sach endpoint public.
- Dam bao response format thong nhat.
- Them authentication bang API key hoac Bearer token.
- Them rate limit co ban.
- Them error response ro rang voi `code`, `message`, `details`.
- Co versioning, vi du `/v1/books`.

### Giai doan 2: Developer portal

- Tao landing page developer portal.
- Them quickstart 5 phut.
- Them API reference.
- Them trang pricing.
- Them trang status/changelog.
- Them form dang ky developer va tao API key.

### Giai doan 3: Sandbox

- Tao sandbox base URL rieng, vi du `https://sandbox.api.example.com`.
- Dung du lieu mau.
- Cho developer test ma khong anh huong production.
- Cung cap sample API key.
- Them Postman collection hoac curl examples.

### Giai doan 4: Launch

- Moi mot nhom developer nho dung thu.
- Thu feedback ve docs, flow dang ky va loi tich hop.
- Theo doi KPI activation va error rate.
- Sua docs/API truoc khi cong bo rong hon.

## 7. Mo hinh kiem tien de xuat

### Phuong an khuyen nghi: Freemium + Tiered pricing

| Goi | Gia | Gioi han | Phu hop voi |
| --- | --- | --- | --- |
| Free | 0 VND | 1,000 calls/thang, sandbox, community support | Sinh vien, demo, thu nghiem |
| Pro | 199,000 VND/thang | 50,000 calls/thang, production API, email support | App nho, nhom lap trinh |
| Business | 999,000 VND/thang | 500,000 calls/thang, analytics, SLA co ban | Truong hoc, thu vien nho |
| Enterprise | Lien he | Custom quota, dedicated support, custom SLA | To chuc lon |

### Ly do chon

- Free plan giup tang developer signup va adoption.
- Pro/Business giup kiem tien khi developer co nhu cau that.
- Enterprise de linh hoat voi khach hang lon.
- De gan KPI: signup, activation, call volume, conversion.

## 8. Thiet ke developer portal don gian

### Cau truc trang

```text
Developer Portal
+-- Home
+-- Quickstart
+-- API Reference
+-- Sandbox
+-- Pricing
+-- Analytics
+-- Changelog
+-- Support
```

### Noi dung man hinh Home

- Ten API va mo ta ngan gon.
- Nut `Get API Key`.
- Nut `View Docs`.
- 3 loi ich chinh:
  - Easy integration
  - Reliable API
  - Clear pricing
- Doan code mau goi API dau tien.

### Noi dung Quickstart

1. Dang ky developer account.
2. Tao API key.
3. Goi endpoint dau tien.
4. Xu ly loi co ban.
5. Chuyen tu sandbox sang production.

Vi du request:

```bash
curl -X GET "https://sandbox.api.example.com/v1/books" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Noi dung API Reference

| Method | Endpoint | Muc dich |
| --- | --- | --- |
| `GET` | `/v1/books` | Lay danh sach sach |
| `GET` | `/v1/books/{id}` | Lay chi tiet sach |
| `POST` | `/v1/books` | Tao sach moi |
| `PATCH` | `/v1/books/{id}` | Cap nhat sach |
| `DELETE` | `/v1/books/{id}` | Xoa sach |

### Noi dung Sandbox

- Base URL sandbox.
- Sample API key.
- Du lieu mau.
- Postman collection.
- Curl examples.
- Luu y: sandbox co the reset du lieu moi ngay.

### Noi dung Analytics

- Bieu do call volume theo ngay.
- Bieu do error rate.
- Bang top endpoints.
- Latency trung binh va p95.
- Quota da dung / quota con lai.

## 9. Checklist hoan thanh

- [ ] Xac dinh API cua nhom dang lam la san pham cho ai.
- [ ] Viet value proposition cho API.
- [ ] Hoan thanh business model canvas.
- [ ] Chon KPI chinh: signup, call volume, error rate.
- [ ] De xuat pricing model.
- [ ] Thiet ke sitemap developer portal.
- [ ] Viet quickstart don gian.
- [ ] Liet ke endpoint API reference.
- [ ] Mo ta sandbox va cach cap API key.
- [ ] Chuan bi slide hoac file demo developer portal.

## 10. Giai y trinh bay

- Mo dau: "API khong chi la backend endpoint, ma la san pham cho developer."
- Noi ve khach hang muc tieu va gia tri API mang lai.
- Trinh bay business model canvas.
- Trinh bay developer journey: dang ky -> lay API key -> test sandbox -> production.
- Trinh bay pricing va KPI.
- Ket luan bang rui ro va cach theo doi:
  - Docs kho hieu -> do activation rate.
  - API loi nhieu -> do error rate.
  - Khong co doanh thu -> do conversion rate.

