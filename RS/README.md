# Movie Recommendation System

Hệ thống gợi ý phim sử dụng 3 phương pháp: Collaborative Filtering, Content-based Filtering và Hybrid Filtering.

## Demo sản phẩm
- [YouTube Playlist Demo](https://youtube.com/playlist?list=PLTLFf7oAFMDWfZdUEbh4YydTBObRMuIKI&si=UjXwpBf0DYqjUO3u)

## Cấu trúc Project
```
app/
├── models/         # Chứa các model gợi ý
├── views/          # Giao diện người dùng (Streamlit)
├── controllers/    # Xử lý logic
├── data/           # Dữ liệu và tiền xử lý
└── utils/          # Các tiện ích
```

## Cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/TrinhHuuTho/NLP_Course
   cd RS
   ```
2. (Khuyến nghị) Tạo môi trường ảo:
   ```bash
   python -m venv .venv
   # Kích hoạt môi trường ảo
   # Trên Linux/Mac
   source .venv/bin/activate
   # Trên Windows
   .venv\Scripts\activate
   ```
3. Cài đặt các thư viện:
   ```bash
   pip install -r requirements.txt
   ```
4. Cấu hình biến môi trường:
   - Tạo file `.env` trong thư mục gốc của dự án
   - Thêm các biến môi trường sau vào file `.env`:
     ```env
     YOUTUBE_API_KEY=your_api_key_here
     ```
   - Thay thế `your_api_key_here` bằng API key của bạn từ Google Cloud Platform. Lưu ý rằng bạn cần kích hoạt API YouTube Data API v3 trong dự án của mình.

## Chạy ứng dụng
```bash
streamlit run app/views/main.py
```

## Tính năng
- Xem trailer phim
- Đánh giá và bình luận phim
- Gợi ý phim dựa trên:
  - Collaborative Filtering
  - Content-based Filtering
  - Hybrid Filtering

## Liên hệ
- **Tên:** Trịnh Hữu Thọ
- **Email:** trinhuutho@gmail.com
- **GitHub:** [https://github.com/TrinhHuuTho](https://github.com/TrinhHuuTho)
