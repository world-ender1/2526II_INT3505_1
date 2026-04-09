from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

app = Flask(__name__)

# Kết nối CSDL phục vụ API
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['pagination_demo']
collection = db['logs']

print('🔗 Đã kết nối DB phục vụ API Flask')

# Tối ưu JSON trả về nếu có object id (Flask không tự json serialize ObjectId)
class PymongoJSONEncoder(app.json_encoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
app.json_encoder = PymongoJSONEncoder

@app.route('/api/offset', methods=['GET'])
def get_offset():
    try:
        page = int(request.args.get('page', 1))
        limit = 20
        skip = (page - 1) * limit
        
        start_time = time.time()
        
        # Cursor của pymongo trả về object cần list() để query thực tế
        cursor = collection.find({}).sort("_id", 1).skip(skip).limit(limit)
        
        # Ép kiểu dữ liệu pymongo ra dict & cast cái obj_id sang string
        data = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            data.append(doc)
            
        end_time = time.time()
        execution_time_ms = round((end_time - start_time) * 1000, 2)
        
        return jsonify({
            "method": "OFFSET (skip & limit)",
            "execution_time_ms": execution_time_ms,
            "page": page,
            "record_count": len(data),
            "data": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cursor', methods=['GET'])
def get_cursor():
    try:
        cursor_id = request.args.get('cursor_id')
        limit = 20
        
        start_time = time.time()
        
        query_cond = {}
        if cursor_id:
            query_cond = {"_id": {"$gt": ObjectId(cursor_id)}}
            
        cursor = collection.find(query_cond).sort("_id", 1).limit(limit)
        
        data = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            data.append(doc)
            
        end_time = time.time()
        execution_time_ms = round((end_time - start_time) * 1000, 2)
        
        next_cursor_id = data[-1]['_id'] if len(data) > 0 else None
        
        return jsonify({
            "method": "CURSOR (using _id)",
            "execution_time_ms": execution_time_ms,
            "next_cursor_id": next_cursor_id,
            "record_count": len(data),
            "data": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy cục bộ
    print("🚀 Khởi chạy Server phân trang bằng Flask port 5000")
    app.run(port=5000, debug=True)
