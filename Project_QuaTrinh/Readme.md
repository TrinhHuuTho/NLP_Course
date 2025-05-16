# Đồ Án Quá Trình Môn Học Natural Language Processing (NLP)

---

## Demo sản phẩm
- [YouTube Demo](https://youtu.be/A4ZkI5JYRDA)

## Giới Thiệu
Dự án này được xây dựng với mục tiêu tổng hợp các kiến thức trong môn Xử lý Ngôn ngữ Tự nhiên (NLP) theo một trình tự logic các bước để xây dựng mô hình NLP. Project nhằm vận dụng các kiến thức đã học vào thực tế thông qua việc xây dựng một website tổng hợp các kiến thức trong suốt môn học.

### Công nghệ được sử dụng
- Python 3.10
- Streamlit
- Pandas, Numpy, Scikit-learn, v.v.

---

## Tính Năng Chính
- Thu thập dữ liệu web từ các nguồn khác nhau: Selenium, BeautifulSoup, Scrapy
- Tăng cường dữ liệu với các kỹ thuật như Data Augmentation: Back Translation, Synonym Replacement, Random Insertion, Random Deletion
- Tiền xử lý dữ liệu văn bản: Xóa dấu câu, Chuyển đổi chữ hoa/thường, Xóa stop words, Stemming, Lemmatization
- Biểu diễn văn bản: One-hot, CountVectorizer, Bag of N-grams, TF-IDF, Word2Vec, GloVe, FastText, ChatGPT, BERT, RoBERTa
- Các mô hình học máy: Logistic Regression, Naive Bayes, Decision Tree, Support Vector Machine (SVM), K-Nearest Neighbors (KNN)

---

## Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.10 trở lên

---

### Hướng Dẫn Cài Đặt

1. Clone repo:
    ```bash
    git clone https://github.com/TrinhHuuTho/NLP_Course.git
    cd NLP_Course/Project_QuaTrinh
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
3. Cài đặt các thư viện phụ thuộc:
    ```bash
    pip install -r requirements.txt
    ```
4. Chạy ứng dụng:
    ```bash
    streamlit run main.py
    ```

---

## Cấu Trúc Thư Mục
```bash
Project_QuaTrinh/
├── main.py               # Điểm bắt đầu chạy app Streamlit
├── models/               # Tầng Model (xử lý dữ liệu, business logic)
├── views/                # Tầng View (hiển thị giao diện Streamlit)
├── controllers/          # Tầng Controller (điều phối logic giữa Model và View)
├── utils/                # Thư viện phụ trợ (helper functions, configs, constants)
└── requirements.txt      # Các thư viện cần cài
```

---

## Liên Hệ
- **Tên:** Trịnh Hửu Thọ
- **Email:** trinhuutho@gmail.com
- **GitHub:** [https://github.com/TrinhHuuTho](https://github.com/TrinhHuuTho)

---

