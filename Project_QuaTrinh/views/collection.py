from controllers.data_collection import DataDownloader
import streamlit as st
import pandas as pd

def scraper_view():
    st.title("🌐 Web Scraper - Thu thập dữ liệu từ trang web")

    # Kiểm tra session state để tránh reset khi UI cập nhật
    if "scraper" not in st.session_state:
        st.session_state.scraper = DataDownloader()
    if "sub_classes" not in st.session_state:
        st.session_state.sub_classes = []
    if "all_classes" not in st.session_state:
        st.session_state.all_classes = []

    # Nhập URL
    url = st.text_input("🔗 Nhập URL của trang web:")

    if url and st.button("📥 Tải trang web"):
        html_preview = st.session_state.scraper.fetch_webpage(url)

        with st.expander("📌 Bấm vào đây để xem chi tiết html"):
            st.code(html_preview, language="html")  # Hiển thị HTML tải về
        st.session_state.all_classes = st.session_state.scraper.get_all_classes()  # Lấy danh sách class

    if st.session_state.all_classes:
        st.markdown("### 🏷 Chọn danh sách chính")

        # Chọn danh sách chính (bắt buộc)
        list_class = st.selectbox("📌 Chọn class chứa danh sách chính:", st.session_state.all_classes)

        # Nút để quét danh sách class con (chỉ chạy khi nhấn)
        if st.button("🔍 Quét danh sách con"):
            st.session_state.sub_classes = st.session_state.scraper.get_sub_classes(list_class)

    if st.session_state.sub_classes:
        st.markdown("### 🏷 Chọn cột dữ liệu từ danh sách con")

        # Chọn cột dữ liệu (chỉ chọn từ danh sách con)
        column_classes = []
        for i in range(5):
            col_class = st.selectbox(f"📝 Chọn class của cột {i+1}:", ["Không chọn"] + st.session_state.sub_classes, key=f"col_{i}")
            if col_class != "Không chọn":
                column_classes.append(col_class)

        # Chỉ chạy khi nhấn nút "📊 Lấy dữ liệu"
        if list_class and column_classes and st.button("📊 Lấy dữ liệu"):
            df = st.session_state.scraper.extract_data(list_class, column_classes)

            if isinstance(df, pd.DataFrame) and not df.empty:
                st.dataframe(df)  # Hiển thị dữ liệu dạng bảng
                st.download_button("💾 Tải xuống CSV", data=df.to_csv(index=False), file_name="data.csv")
            else:
                st.warning("⚠️ Không tìm thấy dữ liệu. Hãy kiểm tra lại danh sách và cột bạn đã chọn.")
