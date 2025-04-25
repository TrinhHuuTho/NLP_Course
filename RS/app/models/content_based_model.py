import pandas as pd
import numpy as np
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.movie_model import MovieModel

class ContentBasedModel:
    def __init__(self):
        self.movie_model = MovieModel()
        self.tfidf_matrix = None
        self.movie_similarity = None
        self.movies_df = None
        self._build_model()
    
    def _build_model(self):
        """
        Xây dựng ma trận TF-IDF và tính toán độ tương đồng giữa các phim
        """
        try:
            # Kiểm tra xem file movies.csv có tồn tại không
            if not os.path.exists('app/data/movies_processed.csv'):
                raise FileNotFoundError("File movies_processed.csv not found in app/data/")
            
            # Đọc dữ liệu phim
            self.movies_df = pd.read_csv('app/data/movies_processed.csv')
            
            # Kiểm tra các cột cần thiết
            required_columns = ['title', 'overview', 'genres']
            missing_columns = [col for col in required_columns if col not in self.movies_df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in movies.csv: {missing_columns}")
            
            # Kết hợp các thuộc tính văn bản của phim
            self.movies_df['content'] = self.movies_df['overview'].fillna('') + ' ' + \
                                      self.movies_df['genres'].fillna('')
            
            # Tạo ma trận TF-IDF
            tfidf = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = tfidf.fit_transform(self.movies_df['content'])
            
            # Tính toán độ tương đồng giữa các phim
            self.movie_similarity = cosine_similarity(self.tfidf_matrix)
            
        except Exception as e:
            print(f"Error building content-based model: {str(e)}")
            self.tfidf_matrix = None
            self.movie_similarity = None
            self.movies_df = pd.DataFrame()
    
    def get_recommendations(self, movie_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Content-based Filtering
        """
        if self.movie_similarity is None or self.movies_df.empty:
            return []
            
        if movie_id is None:
            # Nếu không có movie_id, lấy phim có đánh giá cao nhất
            movie_id = self.movie_model.ratings_df.groupby('movieId')['rating'].mean().idxmax()
        
        # Lấy index của phim trong ma trận
        movie_idx = self.movies_df[self.movies_df['id'] == movie_id].index[0]
        
        # Lấy độ tương đồng với phim được chọn
        movie_similarities = self.movie_similarity[movie_idx]
        
        # Lấy top N phim tương tự
        similar_movie_indices = movie_similarities.argsort()[::-1][1:n_recommendations+1]
        similar_movies = self.movies_df.iloc[similar_movie_indices]
        
        # Thêm thông tin độ tương đồng vào kết quả
        recommendations = []
        for idx, movie in similar_movies.iterrows():
            movie_dict = movie.to_dict()
            movie_dict['similarity_score'] = movie_similarities[idx]
            recommendations.append(movie_dict)
        
        return recommendations 