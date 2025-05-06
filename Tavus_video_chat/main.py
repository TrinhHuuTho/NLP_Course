from tavus_api import get_conversation, end_conversation
from dotenv import load_dotenv
import os
import webbrowser

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API key và Conversation ID từ biến môi trường
API_KEY = os.getenv('TAVUS_API_KEY')
CONVERSATION_ID = os.getenv('TAVUS_CONVERSATION_ID')

if __name__ == "__main__":
    # Kiểm tra xem các biến môi trường đã được cấu hình chưa
    if not API_KEY or not CONVERSATION_ID:
        print("Lỗi: Vui lòng cấu hình TAVUS_API_KEY và TAVUS_CONVERSATION_ID trong file .env")
        exit(1)

    # Lấy thông tin cuộc trò chuyện
    info = get_conversation(CONVERSATION_ID, API_KEY)
    if not info:
        print("Không thể lấy thông tin cuộc trò chuyện. Vui lòng kiểm tra lại API key và Conversation ID.")
        exit(1)
    print("Thông tin cuộc trò chuyện:", info)

    # Mở URL cuộc trò chuyện trong trình duyệt
    if 'conversation_url' in info:
        print(f"\nĐang mở cuộc trò chuyện tại: {info['conversation_url']}")
        webbrowser.open(info['conversation_url'])
    else:
        print("Không tìm thấy URL cuộc trò chuyện")

    # Kết thúc cuộc trò chuyện (nếu muốn)
    # result = end_conversation(CONVERSATION_ID, API_KEY)
    # if result:
    #     print("Kết thúc cuộc trò chuyện:", result)
    # else:
    #     print("Không thể kết thúc cuộc trò chuyện")