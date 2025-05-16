# Tavus AI Video Chat

Dự án này là một ứng dụng chat video sử dụng Tavus API để tạo và quản lý các cuộc trò chuyện video với AI.

## Demo sản phẩm
- [YouTube Demo](https://www.youtube.com/watch?v=slmWqineseI)

## Tính năng

- Tạo và quản lý cuộc trò chuyện video với Tavus AI
- Lấy thông tin chi tiết về cuộc trò chuyện
- Kết thúc cuộc trò chuyện khi cần thiết

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Kết nối internet
- API key từ Tavus

## Cài đặt

1. Clone repository này về máy của bạn:
   ```bash
   git clone https://github.com/TrinhHuuTho/NLP_Course
   cd Tavus_video_chat
   ```
2. (Khuyến nghị) Tạo môi trường ảo:
   ```bash
   python -m venv .venv
   # Kích hoạt môi trường ảo
   # Trên Linux/Mac
   source .venv/bin/activate
   # Trên Windows
   .venv\Scripts\activate
   ```
3. Cài đặt các dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Cấu hình biến môi trường:
   - Tạo file `.env` trong thư mục gốc của dự án
   - Thêm các biến môi trường sau vào file `.env`:
     ```env
     TAVUS_API_KEY=your_api_key_here
     TAVUS_CONVERSATION_ID=your_conversation_id_here
     ```
   - Thay thế `your_api_key_here` bằng API key của bạn từ Tavus
   - Thay thế `your_conversation_id_here` bằng ID cuộc trò chuyện của bạn

## Sử dụng

1. Chạy ứng dụng:
   ```bash
   python main.py
   ```
2. Ứng dụng sẽ:
   - Lấy thông tin về cuộc trò chuyện hiện tại
   - Hiển thị thông tin chi tiết về cuộc trò chuyện
   - (Tùy chọn) Kết thúc cuộc trò chuyện khi cần

## API Endpoints

Dự án sử dụng các endpoints sau từ Tavus API:
- `GET /v2/conversations/{conversation_id}`: Lấy thông tin cuộc trò chuyện
- `POST /v2/conversations/{conversation_id}/end`: Kết thúc cuộc trò chuyện

## Lưu ý

- Đảm bảo bạn có API key hợp lệ từ Tavus
- Giữ API key của bạn an toàn và không chia sẻ nó
- Kiểm tra kết nối internet trước khi sử dụng ứng dụng

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp.

## Liên hệ
- **Tên:** Trịnh Hữu Thọ
- **Email:** trinhuutho@gmail.com
- **GitHub:** [https://github.com/TrinhHuuTho](https://github.com/TrinhHuuTho)

## Giấy phép

MIT License