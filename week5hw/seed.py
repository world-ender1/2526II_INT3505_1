import time
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timezone

# Khởi tạo kết nối DB cục bộ
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['pagination_demo']
collection = db['logs']

def seed_data():
    print(" Đã kết nối đến Database")
    
    # Xoá database cũ
    collection.delete_many({})
    print(" Đã dọn sạch dữ liệu cũ")
    
    # Đánh Index cho _id (Mặc định _id trong MongoDB đã được đánh Index, ta Explicit khai báo cho an tâm)
    collection.create_index([("_id", ASCENDING)])
    
    total_records = 1000000
    batch_size = 10000
    batches = total_records // batch_size
    
    print(f" Bắt đầu nhồi {total_records:,} bản ghi (Gồm {batches} lô)...")
    start_time = time.time()
    
    for i in range(batches):
        fake_data = []
        for j in range(batch_size):
            current_idx = i * batch_size + j
            # Lưu ý dùng chuẩn naming Python thay vì CamelCase
            fake_data.append({
                "index": current_idx,
                "message": f"Dòng log số {current_idx}",
                "created_at": datetime.now(timezone.utc)
            })
        
        # Chèn lô 10k bản ghi
        collection.insert_many(fake_data)
        
        # Log tiến trình
        print(f"\rĐang xử lý lô thứ {i + 1}/{batches}...", end="")
        
    end_time = time.time()
    print(f"\n Hoàn tất Seed Data! (Mất {round(end_time - start_time, 2)} giây)")
    
if __name__ == '__main__':
    seed_data()
