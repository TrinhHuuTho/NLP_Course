from views.home import Header, Menu, Body, Footer
from views.augumentation import augmentation_view
from views.collection import scraper_view

import streamlit as st
import nltk
nltk.download('averaged_perceptron_tagger_eng')

def main():
    choice = Menu()
    # Điều hướng đến từng view
    if choice == "🏠 Trang chủ":
        Header() 
        Body()
        Footer()

    elif choice == "📝 Tăng cường dữ liệu":
        augmentation_view()

    elif choice == "📥 Thu thập dữ liệu":
        scraper_view()

    elif choice == "🔍 Tiền xử lý dữ liệu":
        st.text("Đang phát triển")

    elif choice == "📊 Trực quan hóa dữ liệu":
        st.text("Đang phát triển")

    elif choice == "📞 Liên hệ":
        st.text("Đang phát triển")

    elif choice == "❌ Thoát":
        st.info("Cảm ơn bạn đã dùng chương trình")
        st.stop()


if __name__ == "__main__":
    main()
