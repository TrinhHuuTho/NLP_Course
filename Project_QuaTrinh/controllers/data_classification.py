import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datasets import load_dataset  # Hugging Face Datasets
import time
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.utils import shuffle # Đảo ngẫu nhiên dữ liệu
import pickle  # Thư viện này để lưu model

class TextClassifier:
    def __init__(self, dataset_name, model_type, n_neighbors):
        """Khởi tạo bộ phân loại văn bản"""
        self.dataset_name = dataset_name
        self.model_type = model_type
        self.n_neighbors = n_neighbors
        self.vectorizer = TfidfVectorizer(max_features=5000)  # Chuyển đổi văn bản thành vector TF-IDF
        self.model = None

        # self.train_labels = None
        # self.train_texts = None
        # self.test_labels = None
        # self.test_texts = None

        self.text_column = None
        self.label_column = None

        self._load_dataset()
    
    def _load_dataset(self):
        """Tải dataset từ Hugging Face"""
        dataset_mapping = {
            # "SST": "sst", # config mặc định không có column thuộc kiểu string
            "IMDb Review": "imdb",
            "Yelp Review": "yelp_review_full",
            "Amazon Review": "amazon_polarity",
            "TREC": "trec",
            "Yahoo! Answer": "yahoo_answers_topics",
            "AG's News": "ag_news",
            "Sogou News": "sogou_news",
            "DBPedia": "dbpedia_14"
        }
        
        if self.dataset_name not in dataset_mapping:
            raise ValueError("❌ Dataset không hợp lệ!")

        dataset = load_dataset(dataset_mapping[self.dataset_name], trust_remote_code=True)

        # Tìm cột chứa văn bản
        sample = dataset["train"][0]
        for col in sample.keys():
            if isinstance(sample[col], str):  # Cột có kiểu dữ liệu là chuỗi
                self.text_column = col
                break
        
        # Tìm cột chứa nhãn
        for col in sample.keys():
            unique_values = set(dataset["train"][col])
            if len(unique_values) < 20 and isinstance(list(unique_values)[0], (int, str)):  # Cột có ít giá trị duy nhất
                self.label_column = col
                break

        if not self.text_column or not self.label_column:
            raise ValueError("⚠️ Không xác định được cột văn bản hoặc nhãn!")

        # Lấy dữ liệu
        self.train_texts, self.train_labels = dataset["train"][self.text_column], dataset["train"][self.label_column]
        self.test_texts, self.test_labels = dataset["test"][self.text_column], dataset["test"][self.label_column]

    def train_model(self, progress_bar):
        """Huấn luyện mô hình"""
        start_time = time.time()

        # 1. Vector hóa dữ liệu
        X_train = self.vectorizer.fit_transform(self.train_texts)
        X_test = self.vectorizer.transform(self.test_texts)

        y_train = np.array(self.train_labels)
        y_test = np.array(self.test_labels)

        # 2️⃣ Chọn mô hình phù hợp
        model_mapping = {
            "Naive Bayes": MultinomialNB(),
            "Logistic Regression": LogisticRegression(max_iter=200),
            "SVM": SVC(kernel='linear'),
            "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=self.n_neighbors),
            "Decision Tree": DecisionTreeClassifier()
        }

        if self.model_type not in model_mapping:
            raise ValueError("❌ Thuật toán không hợp lệ!")

        self.model = model_mapping[self.model_type]

        # 3️⃣ Huấn luyện mô hình trên toàn bộ dữ liệu
        self.model.fit(X_train, y_train)

        if progress_bar:
            progress_bar.progress(1.0)  # Cập nhật tiến trình hoàn thành

        train_time = time.time() - start_time  # Đo thời gian train thực tế

        # 5️⃣ Kiểm tra độ chính xác
        y_pred = self.model.predict(X_test)
        # Tính toán accuracy, precision, recall, và f1-score
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Lưu các thông số vào model_data
        model_data = {   
            "train_time":train_time,
            "accuracy": accuracy, 
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }

        # 6️⃣ Lưu model đã train vào file
        with open(f"pre-trained/{self.model_type}/{self.model_type}_{self.dataset_name}.pkl", "wb") as f:
            pickle.dump((self.model, self.vectorizer, model_data), f)

        return accuracy, train_time  # Trả về độ chính xác + thời gian train thực tế

    def simulate_training_step(self, progress_bar, train_time):
        """Cập nhật progress bar theo thời gian train thực tế"""
        step_duration = train_time / 100  # Chia nhỏ thời gian thực tế ra 100 bước
        for i in range(1, 101):
            time.sleep(step_duration)
            progress_bar.progress(i / 100.0)  # Cập nhật progress bar trong view

    def predict(self, text):
        """Dự đoán phân loại văn bản"""
        try:
        # ✅ Tải model đã lưu
            with open(f"pre-trained/{self.model_type}/{self.model_type}_{self.dataset_name}.pkl", "rb") as f:
                self.model, self.vectorizer, self.model_data = pickle.load(f)

            X_text = self.vectorizer.transform(text)
            prediction = self.model.predict(X_text)
            return prediction
        except FileNotFoundError:
            raise ValueError("⚠️ Model chưa được train! Vui lòng train trước khi dự đoán.")