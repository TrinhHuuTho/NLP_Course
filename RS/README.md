# Movie Recommendation System

Hệ thống gợi ý phim sử dụng 3 phương pháp: Collaborative Filtering, Content-based Filtering và Hybrid Filtering.

## Cấu trúc Project
```
app/
├── models/         # Chứa các model gợi ý
├── views/          # Giao diện người dùng (Streamlit)
├── controllers/    # Xử lý logic
├── data/          # Dữ liệu và tiền xử lý
└── utils/         # Các tiện ích
```

## Cài đặt
1. Clone repository
2. Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

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