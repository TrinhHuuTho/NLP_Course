# AI Web Scraper with Gemini

Một ứng dụng web scraper thông minh sử dụng Google Gemini API để trích xuất dữ liệu có cấu trúc từ các trang web. Ứng dụng này có thể phân tích nội dung HTML và chuyển đổi thành định dạng CSV dựa trên yêu cầu của người dùng.

## Demo sản phẩm
- [YouTube Demo](https://www.youtube.com/watch?v=tBxsD9z0wAA)

## Tính năng

- 🌐 Scrape dữ liệu từ bất kỳ trang web nào
- 🤖 Sử dụng Google Gemini AI để phân tích nội dung
- 📊 Xuất dữ liệu sang định dạng CSV
- 🔍 Trích xuất thông tin có cấu trúc từ HTML
- 🧹 Tự động làm sạch và xác thực dữ liệu
- 📱 Giao diện web thân thiện với người dùng

## Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/TrinhHuuTho/NLP_Course
   cd Web Scraper
   ```
2. (Khuyến nghị) Tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```
3. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
4. Tạo file `.env` và thêm API key của Google Gemini:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

## Sử dụng

1. Khởi động ứng dụng:
   ```bash
   streamlit run main.py
   ```
2. Truy cập ứng dụng qua trình duyệt web (mặc định: http://localhost:8501)
3. Nhập URL của trang web cần scrape
4. Mô tả dữ liệu bạn muốn trích xuất (ví dụ: "danh sách phim với tên, rating và số lượng đánh giá")
5. Nhấn "Extract Data" và đợi kết quả
6. Tải xuống dữ liệu dưới dạng file CSV

## Cấu trúc Project

```
web-scraper/
├── main.py              # Entry point và Streamlit UI
├── scrape.py           # Logic scraping website
├── gemini_parser.py    # Xử lý Gemini API và dữ liệu
├── requirements.txt    # Các thư viện phụ thuộc
├── .env               # Cấu hình API key
└── README.md          # Tài liệu hướng dẫn
```

## Ví dụ Sử dụng

### Trích xuất thông tin phim:
```
Mô tả: "Tôi muốn lấy danh sách phim bao gồm tên phim, rating trung bình và tổng số lượt đánh giá"

Kết quả:
Movie Name,Average Rating,Total Ratings
The Shawshank Redemption,9.3,2500000
The Godfather,9.2,1800000
...
```

## Yêu cầu Hệ thống

- Python 3.8+
- Google Gemini API key
- Kết nối internet

## Giấy phép

MIT License

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Liên hệ

- **Tên:** Trịnh Hữu Thọ
- **Email:** trinhuutho@gmail.com
- **GitHub:** [https://github.com/TrinhHuuTho](https://github.com/TrinhHuuTho)

## Cảm ơn
- @techwithtim đã cho video hướng dẫn và gợi ý phát triển dự án này