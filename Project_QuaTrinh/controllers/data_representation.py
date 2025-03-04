from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class DataRepresentation:
    def __init__(self, method="count"):
        """
        Khởi tạo vectorizer.
        method: "count" -> CountVectorizer, "onehot" -> One-hot encoding
        """
        self.method = method
        self.vectorizer = None

    def fit_transform(self, texts):
        """Biểu diễn dữ liệu văn bản bằng CountVectorizer hoặc One-hot encoding"""
        if not texts:
            return "⚠️ Không có dữ liệu để biểu diễn!"
        
        if self.method == "count":
            self.vectorizer = CountVectorizer(binary=False)
            transformed = self.vectorizer.fit_transform(texts)
            df = pd.DataFrame(transformed.toarray(), columns=self.vectorizer.get_feature_names_out())
            return df
        
        elif self.method == "onehot":
            self.vectorizer = CountVectorizer(binary=True)  # One-hot encoding = CountVectorizer(binary=True)
            transformed = self.vectorizer.fit_transform(texts)
            df = pd.DataFrame(transformed.toarray(), columns=self.vectorizer.get_feature_names_out())
            return df
        
        else:
            return "❌ Phương thức không hợp lệ!"
