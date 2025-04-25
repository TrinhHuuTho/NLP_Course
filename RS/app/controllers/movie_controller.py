import pandas as pd
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.movie_model import MovieModel

class MovieController:
    def __init__(self):
        self.movie_model = MovieModel()
    
    def search_movies(self, query):
        """
        Tìm kiếm phim dựa trên query
        """
        return self.movie_model.search_movies(query)
    
    def get_movie_by_id(self, movie_id):
        """
        Lấy thông tin phim theo ID
        """
        return self.movie_model.get_movie_by_id(movie_id)
    
    def add_review(self, movie_id, rating, review):
        """
        Thêm đánh giá và bình luận cho phim
        """
        return self.movie_model.add_review(movie_id, rating, review)
    
    def get_movie_reviews(self, movie_id):
        """
        Lấy danh sách đánh giá và bình luận của phim
        """
        return self.movie_model.get_movie_reviews(movie_id) 