import pandas as pd
import numpy as np
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.collaborative_model import CollaborativeModel
from app.models.content_based_model import ContentBasedModel

class HybridModel:
    def __init__(self):
        self.collaborative_model = CollaborativeModel()
        self.content_based_model = ContentBasedModel()
    
    def get_recommendations(self, user_id=None, movie_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Hybrid Filtering
        Kết hợp cả Collaborative và Content-based để tìm các phim phù hợp nhất
        """
        # Lấy gợi ý từ Collaborative Filtering
        collab_recommendations = self.collaborative_model.get_recommendations(user_id, n_recommendations * 2)
        collab_movie_ids = {movie['id'] for movie in collab_recommendations}
        
        # Lấy gợi ý từ Content-based Filtering
        content_recommendations = self.content_based_model.get_recommendations(movie_id, n_recommendations * 2)
        content_movie_ids = {movie['id'] for movie in content_recommendations}
        
        # Tìm phần giao giữa hai tập gợi ý
        common_movie_ids = collab_movie_ids.intersection(content_movie_ids)
        
        # Nếu không có đủ phim trong phần giao, thêm các phim có điểm cao từ cả hai phương pháp
        if len(common_movie_ids) < n_recommendations:
            # Tính điểm tổng hợp cho mỗi phim
            movie_scores = {}
            
            # Thêm điểm từ Collaborative Filtering
            for movie in collab_recommendations:
                movie_scores[movie['id']] = movie.get('predicted_rating', 0)
            
            # Thêm điểm từ Content-based Filtering
            for movie in content_recommendations:
                if movie['id'] in movie_scores:
                    movie_scores[movie['id']] += movie.get('similarity_score', 0)
                else:
                    movie_scores[movie['id']] = movie.get('similarity_score', 0)
            
            # Sắp xếp phim theo điểm tổng hợp
            sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Lấy top N phim
            top_movie_ids = [movie_id for movie_id, _ in sorted_movies[:n_recommendations]]
            
            # Lấy thông tin chi tiết của các phim
            final_recommendations = []
            for movie_id in top_movie_ids:
                movie_info = self.content_based_model.movies_df[self.content_based_model.movies_df['id'] == movie_id].iloc[0]
                final_recommendations.append(movie_info.to_dict())
        else:
            # Lấy thông tin chi tiết của các phim trong phần giao
            final_recommendations = []
            for movie_id in list(common_movie_ids)[:n_recommendations]:
                movie_info = self.content_based_model.movies_df[self.content_based_model.movies_df['id'] == movie_id].iloc[0]
                final_recommendations.append(movie_info.to_dict())
        
        return final_recommendations 