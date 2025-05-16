from tavus_api import get_conversation, end_conversation, create_conversation
from dotenv import load_dotenv
import os
import webbrowser

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API key và Conversation ID từ biến môi trường
API_KEY = os.getenv('TAVUS_API_KEY')
CONVERSATION_ID = os.getenv('TAVUS_CONVERSATION_ID')

if __name__ == "__main__":
    # Kiểm tra xem API_KEY đã được cấu hình chưa
    if not API_KEY:
        print("Lỗi: Vui lòng cấu hình TAVUS_API_KEY trong file .env")
        exit(1)

    print("1. Tạo mới cuộc trò chuyện")
    print("2. Xem thông tin cuộc trò chuyện hiện tại")
    print("3. Kết thúc cuộc trò chuyện hiện tại")
    choice = input("Chọn chức năng (1/2/3): ").strip()

    if choice == "1":
        # Tạo mới cuộc trò chuyện
        info = create_conversation(API_KEY)
        if info:
            print("Tạo cuộc trò chuyện thành công:", info)
            if 'conversation_url' in info:
                print(f"\nĐang mở cuộc trò chuyện tại: {info['conversation_url']}")
                webbrowser.open(info['conversation_url'])
            else:
                print("Không tìm thấy URL cuộc trò chuyện")
        else:
            print("Không thể tạo cuộc trò chuyện mới. Vui lòng kiểm tra lại API key.")
    elif choice == "2":
        # Xem thông tin cuộc trò chuyện hiện tại
        if not CONVERSATION_ID:
            print("Lỗi: Vui lòng cấu hình TAVUS_CONVERSATION_ID trong file .env")
            exit(1)
        info = get_conversation(CONVERSATION_ID, API_KEY)
        if not info:
            print("Không thể lấy thông tin cuộc trò chuyện. Vui lòng kiểm tra lại API key và Conversation ID.")
            exit(1)
        print("Thông tin cuộc trò chuyện:", info)
        if 'conversation_url' in info:
            print(f"\nĐang mở cuộc trò chuyện tại: {info['conversation_url']}")
            webbrowser.open(info['conversation_url'])
        else:
            print("Không tìm thấy URL cuộc trò chuyện")
    elif choice == "3":
        # Kết thúc cuộc trò chuyện hiện tại
        if not CONVERSATION_ID:
            print("Lỗi: Vui lòng cấu hình TAVUS_CONVERSATION_ID trong file .env")
            exit(1)
        result = end_conversation(CONVERSATION_ID, API_KEY)
        if result:
            print("Kết thúc cuộc trò chuyện:", result)
        else:
            print("Không thể kết thúc cuộc trò chuyện")
    else:
        print("Lựa chọn không hợp lệ.")