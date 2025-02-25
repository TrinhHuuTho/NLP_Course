import streamlit as st

def Header():
    st.title("🚀 NLP Project - Xử lý Ngôn ngữ Tự nhiên")
    st.write("Chào mừng bạn đến với ứng dụng NLP! Đây là một dự án môn Xử lý Ngôn ngữ Tự nhiên (NLP).")
    # st.image("nlp_image.jpg", caption="Natural Language Processing", use_column_width=True)

def Menu():
    # Tạo Sidebar menu
    menu = ["Tăng cường dữ liệu",
            "Thu thập dữ liệu",
            "Tiền xử lý dữ liệu",
            "Trực quan hóa dữ liệu",
            "Liên hệ?",
            "Thoát"                   
            ]
    st.sidebar.title("Menu")
    return st.sidebar.selectbox("Chọn chức năng", menu)

def Body():
    with st.container():
        st.video("https://www.youtube.com/watch?v=CMrHM8a3hqw&ab_channel=Simplilearn")
        st.caption("Never give up!")

def Footer():
    st.info("Trang web hiện chỉ hỗ trợ xử lý trên ngôn ngữ Tiếng Anh")