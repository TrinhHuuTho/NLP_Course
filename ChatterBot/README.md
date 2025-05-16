# Vietnamese Chatbot

Một chatbot tiếng Việt được xây dựng bằng Python, sử dụng ChatterBot và Flask. Chatbot này có khả năng học hỏi từ các cuộc hội thoại Facebook và tương tác với người dùng qua giao diện web.

## Demo sản phẩm

*Đang cập nhật ...*

## Tính năng

- Xử lý và học hỏi từ dữ liệu tin nhắn Facebook
- Hỗ trợ tiếng Việt đầy đủ
- Giao diện web thân thiện với người dùng
- Xử lý các phép tính toán và câu hỏi về thời gian
- Khả năng học hỏi và cải thiện từ các cuộc hội thoại

## Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package manager)
- Các thư viện Python (được liệt kê trong requirements.txt)

## Cài đặt & Khởi động nhanh

1. Clone repository:
   ```bash
   git clone https://github.com/TrinhHuuTho/NLP_Course
   cd ChatterBot
   ```
2. Tạo môi trường ảo (khuyến nghị):
   ```bash
   python -m venv .venv
   # Kích hoạt môi trường ảo
   # Trên Linux/Mac
   source .venv/bin/activate
   # Trên Windows
   .venv\Scripts\activate
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## Cấu trúc project

```
.  # Thư mục ChatterBot
├── app.py                 # File chính của ứng dụng Flask
├── process_messages.py    # Script xử lý dữ liệu tin nhắn Facebook
├── requirements.txt       # Danh sách các thư viện cần thiết
├── templates/            # Thư mục chứa các file HTML
│   └── index.html        # Giao diện web
├── vietnamese_corpus/    # Thư mục chứa dữ liệu training
│   └── conversations.yml # File chứa các cuộc hội thoại
└── README.md            # Tài liệu hướng dẫn
```

## Cách sử dụng

1. Xử lý dữ liệu tin nhắn Facebook:
   ```bash
   python process_messages.py
   ```
   Script này sẽ:
   - Đọc các file JSON chứa tin nhắn Facebook
   - Xử lý và làm sạch dữ liệu
   - Tạo file conversations.yml cho việc training

2. Chạy ứng dụng:
   ```bash
   python app.py
   ```
   Ứng dụng sẽ:
   - Train chatbot với dữ liệu đã xử lý
   - Khởi động server web
   - Truy cập http://localhost:5000 để sử dụng chatbot

## Xử lý dữ liệu

File `process_messages.py` thực hiện các chức năng:
- Decode text từ Facebook với nhiều encoding
- Làm sạch text (loại bỏ ký tự đặc biệt, URL, etc.)
- Kiểm tra tính hợp lệ của cuộc hội thoại
- Tạo corpus cho việc training

## Cấu hình Chatbot

Chatbot được cấu hình với các logic adapter:
- BestMatch: Tìm câu trả lời phù hợp nhất
- MathematicalEvaluation: Xử lý các phép tính
- TimeLogicAdapter: Xử lý câu hỏi về thời gian

## Góp ý và báo lỗi

Nếu bạn phát hiện lỗi hoặc có góp ý, vui lòng:
1. Tạo issue mới
2. Mô tả chi tiết vấn đề
3. Cung cấp các bước để tái tạo lỗi (nếu có)

## Giấy phép

Project này được phát hành dưới giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.

## Tác giả

- **Tên:** Trịnh Hửu Thọ
- **Email:** trinhuutho@gmail.com
- **GitHub:** [https://github.com/TrinhHuuTho](https://github.com/TrinhHuuTho)

## Cảm ơn

- ChatterBot team cho thư viện tuyệt vời
- Cộng đồng Python và Flask