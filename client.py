import requests

# Địa chỉ của server Flask (mặc định là port 5000)
url = "http://127.0.0.1:5000/"

try:
    # Gửi yêu cầu GET đến server
    response = requests.get(url)

    # Kiểm tra nếu kết nối thành công (status code 200)
    if response.status_code == 200:
        print("Kết nối thành công!")
        print("Nội dung từ server:", response.text)
    else:
        print("Lỗi từ server:", response.status_code)

except requests.exceptions.ConnectionError:
    print("Không thể kết nối! Hãy chắc chắn server Flask đang chạy.")