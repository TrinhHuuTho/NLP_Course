import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.collaborative_model import CollaborativeModel
from app.models.content_based_model import ContentBasedModel
from app.models.hybrid_model import HybridModel

class RecommendationController:
    def __init__(self):
        self.collaborative_model = CollaborativeModel()
        self.content_based_model = ContentBasedModel()
        self.hybrid_model = HybridModel()
    
    def get_collaborative_recommendations(self, user_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Collaborative Filtering
        """
        return self.collaborative_model.get_recommendations(user_id, n_recommendations)
    
    def get_content_based_recommendations(self, movie_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Content-based Filtering
        """
        return self.content_based_model.get_recommendations(movie_id, n_recommendations)
    
    def get_hybrid_recommendations(self, user_id=None, movie_id=None, n_recommendations=10):
        """
        Lấy gợi ý phim dựa trên Hybrid Filtering
        """
        return self.hybrid_model.get_recommendations(user_id, movie_id, n_recommendations) 