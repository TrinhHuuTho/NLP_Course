import pandas as pd
import numpy as np
import sys
import os
from sklearn.metrics.pairwise import cosine_similarity

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.movie_model import MovieModel

class CollaborativeModel:
    def __init__(self):
        self.movie_model = MovieModel()
        self.ratings_matrix = None
        self.user_similarity = None
        self._build_model()
    
    def _build_model(self):
        """
        Xây dựng ma trận đánh giá và tính toán độ tương đồng giữa người dùng
        """
        try:
            # Kiểm tra xem file ratings.csv có tồn tại không
            if not os.path.exists('app/data/ratings_processed.csv'):
                raise FileNotFoundError("File ratings_processed.csv not found in app/data/")
            
            # Kiểm tra cấu trúc của file ratings.csv
            ratings_df = pd.read_csv('app/data/ratings_processed.csv')
            required_columns = ['userId', 'movieId', 'rating']
            missing_columns = [col for col in required_columns if col not in ratings_df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in ratings.csv: {missing_columns}")
            
            # Tạo ma trận đánh giá (user x movie)
            self.ratings_matrix = ratings_df.pivot(
                index='userId',
                columns='movieId',
                values='rating'
            ).fillna(0)
            
            # Tính toán độ tương đồng giữa người dùng
            self.user_similarity = cosine_similarity(self.ratings_matrix)
            
        except Exception as e:
            print(f"Error building collaborative model: {str(e)}")
            # Tạo ma trận rỗng nếu có lỗi
            self.ratings_matrix = pd.DataFrame()
            self.user_similarity = np.array([])
    
    def get_recommendations(self, user_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Collaborative Filtering
        """
        if self.ratings_matrix.empty:
            return []
            
        if user_id is None:
            # Nếu không có user_id, lấy người dùng có nhiều đánh giá nhất
            user_id = self.ratings_matrix.sum(axis=1).idxmax()
        
        # Lấy các phim chưa được đánh giá bởi người dùng
        user_ratings = self.ratings_matrix.loc[user_id]
        unwatched_movies = user_ratings[user_ratings == 0].index
        
        # Tính toán điểm dự đoán cho các phim chưa xem
        user_idx = self.ratings_matrix.index.get_loc(user_id)
        user_similarities = self.user_similarity[user_idx]
        
        predictions = []
        for movie_id in unwatched_movies:
            movie_ratings = self.ratings_matrix[movie_id]
            # Tính điểm dự đoán dựa trên đánh giá của người dùng tương tự
            pred_rating = np.sum(user_similarities * movie_ratings) / np.sum(np.abs(user_similarities))
            predictions.append((movie_id, pred_rating))
        
        # Sắp xếp và lấy top N phim
        predictions.sort(key=lambda x: x[1], reverse=True)
        top_movies = []
        for movie_id, pred_rating in predictions[:n_recommendations]:
            movie_info = self.movie_model.get_movie_by_id(movie_id)
            if movie_info:
                movie_info['predicted_rating'] = pred_rating
                top_movies.append(movie_info)
        
        return top_movies 