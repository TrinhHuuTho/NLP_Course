from views.home import Header, Menu, Body, Footer
from views.augumentation import augmentation_view
from views.collection import scraper_view
from views.preprocessor import preprocessor_view
from views.representation import representation_view

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
        return augmentation_view()

    elif choice == "📥 Thu thập dữ liệu":
        return scraper_view()

    elif choice == "🔍 Tiền xử lý dữ liệu":
        return preprocessor_view()

    elif choice == "🔢 Biểu diễn dữ liệu":
        return representation_view()

    elif choice == "📞 Liên hệ":
        return Footer()

    # elif choice == "❌ Thoát":
    #     st.info("Cảm ơn bạn đã dùng chương trình")
    #     st.stop()


if __name__ == "__main__":
    main()
