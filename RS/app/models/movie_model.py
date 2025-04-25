import pandas as pd
import os

class MovieModel:
    def __init__(self):
        self.movies_df = pd.read_csv('app/data/movies_processed.csv')
        self.ratings_df = pd.read_csv('app/data/ratings_processed.csv')
        self.reviews_df = pd.read_csv('app/data/reviews.csv') if os.path.exists('app/data/reviews.csv') else pd.DataFrame(columns=['movieId', 'userId', 'rating', 'review'])
    
    def search_movies(self, query):
        """
        Tìm kiếm phim dựa trên query
        """
        return self.movies_df[self.movies_df['title'].str.contains(query, case=False)].to_dict('records')
    
    def get_movie_by_id(self, movie_id):
        """
        Lấy thông tin phim theo ID
        """
        movie = self.movies_df[self.movies_df['id'] == movie_id]
        if not movie.empty:
            return movie.iloc[0].to_dict()
        return None
    
    def add_review(self, movie_id, rating, review):
        """
        Thêm đánh giá và bình luận cho phim
        """
        new_review = pd.DataFrame({
            'movieId': [movie_id],
            'userId': ['user_1'],  # Tạm thời hardcode user_id
            'rating': [rating],
            'review': [review]
        })
        self.reviews_df = pd.concat([self.reviews_df, new_review], ignore_index=True)
        self.reviews_df.to_csv('app/data/reviews.csv', index=False)
        return True
    
    def get_movie_reviews(self, movie_id):
        """
        Lấy danh sách đánh giá và bình luận của phim
        """
        return self.reviews_df[self.reviews_df['movieId'] == movie_id].to_dict('records') 