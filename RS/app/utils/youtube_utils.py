from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Biến toàn cục để theo dõi số lần gọi API
API_CALLS = 0
MAX_API_CALLS = 100  # Giới hạn số lần gọi API

def get_youtube_video(movie_title):
    """
    Tìm kiếm trailer phim trên YouTube sử dụng YouTube API
    """
    global API_CALLS
    
    try:
        # Kiểm tra số lần gọi API
        if API_CALLS >= MAX_API_CALLS:
            st.warning("Đã đạt giới hạn số lần tìm kiếm trailer. Vui lòng thử lại sau.")
            return None
        
        # Tăng số lần gọi API
        API_CALLS += 1
        
        # Khởi tạo YouTube API client
        youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
        
        # Tạo query tìm kiếm với các từ khóa tối ưu
        search_query = f"{movie_title} official trailer HD"
        
        # Tìm kiếm video với các tham số tối ưu
        request = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            maxResults=1,
            videoDuration="short",  # Chỉ tìm video ngắn (trailer)
            relevanceLanguage="en",  # Ưu tiên video tiếng Anh
            order="relevance"  # Sắp xếp theo độ liên quan
        )
        response = request.execute()
        
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        
        return None
    except Exception as e:
        if "quotaExceeded" in str(e):
            st.error("Đã hết hạn mức tìm kiếm YouTube API. Vui lòng thử lại sau.")
        else:
            print(f"Error searching YouTube: {str(e)}")
        return None 