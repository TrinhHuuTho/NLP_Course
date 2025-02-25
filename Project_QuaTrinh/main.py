from views.home import Header, Menu, Body, Footer
from views.augumentation import augmentation_view

import streamlit as st

def main():
    Header() 
    Body()
    Footer()
    choice = Menu()
    # Điều hướng đến từng view
    if choice == "Tăng cường dữ liệu":
        augmentation_view()

    elif choice == "Thu thập dữ liệu":
        st.text("Đang phát triển")

    elif choice == "Tiền xử lý dữ liệu":
        st.text("Đang phát triển")

    elif choice == "Trực quan hóa dữ liệu":
        st.text("Đang phát triển")

    elif choice == "Liên hệ":
        st.text("Đang phát triển")

    elif choice == "Thoát":
        st.info("Cảm ơn bạn đã dùng chương trình")
        st.stop()


if __name__ == "__main__":
    main()

"""
Wep app project quá trình môn học NLP với thư viện Streamlit, xây dựng theo mô hình MVC
Tài liệu tham khảo:
    1. Code mẫu từ giáo viên
    2. Giao diện đồ họa với Streamlit
    3. Chatbot fixbug và sửa lỗi
Link video ghi hình: https://youtu.be/SwWnIjmxOp0
"""