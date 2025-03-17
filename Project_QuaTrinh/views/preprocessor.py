import streamlit as st
from controllers.data_preprocessing import TextPreprocessor  # Import lớp tiền xử lý
import streamlit.components.v1 as components  # Import để hiển thị HTML

def preprocessor_view():
    # ========== Cấu hình giao diện Streamlit ==========
    st.title("🔍 Công cụ Tiền Xử Lý Văn Bản")
    st.write("Nhập văn bản hoặc tải lên file để xử lý")

    # Lựa chọn cách nhập văn bản
    option = st.radio("Chọn nguồn nhập dữ liệu:", ("Nhập văn bản", "Tải file văn bản"))

    text = ""

    if option == "Nhập văn bản":
        text = st.text_area("Nhập văn bản của bạn tại đây:", height=200)

    elif option == "Tải file văn bản":
        uploaded_file = st.file_uploader("📂 Chọn file .txt", type="txt")
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")

    # Nếu có văn bản, tiến hành xử lý
    if text:
        preprocessor = TextPreprocessor(text)

        # ========== Chọn các phương thức tiền xử lý ==========
        st.subheader("⚙️ Chọn các phương thức tiền xử lý")
        selected_methods = st.multiselect(
            "Chọn các tùy chọn tiền xử lý:",
            [
                "Tách câu",
                "Tách từ",
                "Xóa stopwords",
                "Chuyển thành chữ thường",
                "Stemming (Porter)",
                "Lemmatization",
                "POS Tagging",
                "Sửa từ viết tắt",
                "Sửa lỗi chính tả",
                "Nhận diện thực thể (NER)"
            ]
        )

        # ========== Hiển thị biểu đồ NER ==========
        if st.button("📊 Biểu đồ (NER)"):
            st.subheader("📍 Biểu đồ Nhận diện Thực thể (NER)")
            ner_html = preprocessor.visualize_entities()
            components.html(ner_html, height=500, scrolling=True)  # Hiển thị biểu đồ trong Streamlit
    
        # Nút thực hiện xử lý
        if st.button("🚀 Thực hiện"):
            if text.strip():
                st.subheader("📝 Kết quả Xử Lý")

                processed_text = "📌 **Kết quả tiền xử lý:**\n\n"
                
                if "Tách câu" in selected_methods:
                    result = preprocessor.sentence_tokenization()
                    st.write("**📌 Sentence Tokenization:**", result)
                    processed_text += "**📌 Sentence Tokenization:**\n" + str(result) + "\n\n"

                if "Tách từ" in selected_methods:
                    result = preprocessor.word_tokenization()
                    st.write("**📌 Word Tokenization:**", result)
                    processed_text += "**📌 Word Tokenization:**\n" + str(result) + "\n\n"

                if "Xóa stopwords" in selected_methods:
                    result = preprocessor.remove_stopwords_punctuation()
                    st.write("**📌 Remove Stopwords:**", result)
                    processed_text += "**📌 Remove Stopwords:**\n" + str(result) + "\n\n"

                if "Chuyển thành chữ thường" in selected_methods:
                    result = preprocessor.to_lowercase()
                    st.write("**📌 Lowercase Text:**", result)
                    processed_text += "**📌 Lowercase Text:**\n" + str(result) + "\n\n"

                if "Stemming (Porter)" in selected_methods:
                    result = preprocessor.stemming()
                    st.write("**📌 Stemming (Porter):**", result)
                    processed_text += "**📌 Stemming (Porter):**\n" + str(result) + "\n\n"

                if "Lemmatization" in selected_methods:
                    result = preprocessor.lemmatization()
                    st.write("**📌 Lemmatization:**", result)
                    processed_text += "**📌 Lemmatization:**\n" + str(result) + "\n\n"

                if "POS Tagging" in selected_methods:
                    result = preprocessor.pos_tagging()
                    st.write("**📌 POS Tagging:**", result)
                    processed_text += "**📌 POS Tagging:**\n" + str(result) + "\n\n"

                if "Sửa từ viết tắt" in selected_methods:
                    result = preprocessor.expand_contractions()
                    st.write("**📌 Expand Contractions:**", result)
                    processed_text += "**📌 Expand Contractions:**\n" + str(result) + "\n\n"

                if "Sửa lỗi chính tả" in selected_methods:
                    result = preprocessor.correct_spelling()
                    st.write("**📌 Correct Spelling:**", result)
                    processed_text += "**📌 Correct Spelling:**\n" + str(result) + "\n\n"

                if "Nhận diện thực thể (NER)" in selected_methods:
                    result = preprocessor.named_entity_recognition()
                    st.write("📍 Nhận diện Thực thể (NER)", result)
                    processed_text += "**📍 Named Entity Recognition (NER):**\n" + str(result) + "\n\n"

                # ✅ Nút tải xuống kết quả xử lý
                st.download_button(
                    "💾 Tải xuống kết quả",
                    data=processed_text,
                    file_name="processed_text.txt"
                )
            else:
                st.warning("⚠️ Vui lòng nhập văn bản!")

        

