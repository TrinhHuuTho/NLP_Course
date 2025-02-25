import streamlit as st
from controllers.data_augmentation import augmenter

def augmentation_view():
    st.title("📝 Tăng cường dữ liệu văn bản")

    # Nhập văn bản
    text = st.text_area("Nhập văn bản cần tăng cường:")

    # Chọn phương pháp tăng cường
    method = st.selectbox("Chọn phương pháp:", [
        "Thay từ đồng nghĩa",
        "Đảo vị trí từ",
        "Xóa từ",
        "Thêm từ ngẫu nhiên",
        "Dịch ngược"
    ])

    # Xử lý tăng cường
    if st.button("Thực hiện"):
        if text.strip():
            if method == "Thay từ đồng nghĩa":
                result = augmenter.synonym_augmentation(text)
            elif method == "Đảo vị trí từ":
                result = augmenter.swap_words(text)
            elif method == "Xóa từ":
                result = augmenter.delete_words(text)
            elif method == "Thêm từ ngẫu nhiên":
                result = augmenter.insert_words(text)
            elif method == "Dịch ngược":
                result = augmenter.back_translation(text)

            st.subheader("📌 Kết quả:")
            st.text_area("Văn bản sau khi tăng cường:", value="\n".join(result), height=150)

            # ✅ Sửa lỗi tải xuống bằng cách chuyển `list` thành `str`
            st.download_button("💾 Tải xuống", data="\n".join(result), file_name="augmented_text.txt")
        else:
            st.warning("⚠️ Vui lòng nhập văn bản!")
