import pandas as pd
import numpy as np
import os

def preprocess_movies_data():
    """
    Tiền xử lý dữ liệu phim
    """
    print("Đang xử lý dữ liệu phim...")
    
    # Đọc dữ liệu
    movies_df = pd.read_csv('movies_metadata.csv')
    
    # Chọn các cột cần thiết
    selected_columns = ['id', 'title', 'overview', 'genres', 'release_date', 'vote_average', 'vote_count']
    movies_df = movies_df[selected_columns]
    
    # Xử lý dữ liệu null
    movies_df['overview'] = movies_df['overview'].fillna('')
    movies_df['genres'] = movies_df['genres'].fillna('[]')
    movies_df['vote_average'] = movies_df['vote_average'].fillna(0)
    movies_df['vote_count'] = movies_df['vote_count'].fillna(0)
    movies_df['release_date'] = movies_df['release_date'].fillna('')
    
    # Trích xuất năm từ ngày phát hành
    movies_df['year'] = pd.to_datetime(movies_df['release_date'], errors='coerce').dt.year
    movies_df['year'] = movies_df['year'].fillna(0).astype(int)
    
    # Chuyển đổi id thành số nguyên
    movies_df['id'] = pd.to_numeric(movies_df['id'], errors='coerce')
    movies_df = movies_df.dropna(subset=['id'])
    movies_df['id'] = movies_df['id'].astype(int)
    
    # Lọc phim có đánh giá
    movies_df = movies_df[movies_df['vote_count'] > 0]
    
    # Sắp xếp theo số lượng đánh giá và lấy top 5000 phim
    movies_df = movies_df.sort_values('vote_count', ascending=False).head(5000)
    
    # Lưu kết quả
    movies_df.to_csv('movies_processed.csv', index=False)
    print(f"Đã xử lý xong dữ liệu phim. Số lượng phim: {len(movies_df)}")

def preprocess_ratings_data():
    """
    Tiền xử lý dữ liệu đánh giá
    """
    print("Đang xử lý dữ liệu đánh giá...")
    
    # Đọc dữ liệu
    ratings_df = pd.read_csv('ratings_small.csv')
    
    # Lọc các đánh giá cho các phim đã chọn
    movies_df = pd.read_csv('movies_processed.csv')
    valid_movie_ids = set(movies_df['id'])
    ratings_df = ratings_df[ratings_df['movieId'].isin(valid_movie_ids)]
    
    # Lọc người dùng có nhiều đánh giá
    user_rating_counts = ratings_df['userId'].value_counts()
    active_users = user_rating_counts[user_rating_counts >= 20].index
    ratings_df = ratings_df[ratings_df['userId'].isin(active_users)]
    
    # Lưu kết quả
    ratings_df.to_csv('ratings_processed.csv', index=False)
    print(f"Đã xử lý xong dữ liệu đánh giá. Số lượng đánh giá: {len(ratings_df)}")

def main():
    # Tạo thư mục data nếu chưa tồn tại
    if not os.path.exists('app/data'):
        os.makedirs('app/data')
    
    # Di chuyển vào thư mục data
    os.chdir('app/data')
    
    # Tiền xử lý dữ liệu
    preprocess_movies_data()
    preprocess_ratings_data()
    
    print("Hoàn thành tiền xử lý dữ liệu!")

if __name__ == "__main__":
    main() 