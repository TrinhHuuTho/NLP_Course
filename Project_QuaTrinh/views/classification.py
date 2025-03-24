import streamlit as st
from controllers.data_classification import TextClassifier

def classification_view():
    tab1, tab2 = st.tabs(["Phân loại", "Hướng dẫn "])
    with tab1:
        st.title("📚 Text Classification - Phân loại văn bản")

        # Chọn dataset
        dataset_list = [
            "IMDb Review", "Yelp Review", "Amazon Review", 
            "TREC", "Yahoo! Answer", "AG's News", "Sogou News", "DBPedia"
        ]
        dataset_name = st.selectbox("🗂 Chọn Dataset", dataset_list)

        # Chọn thuật toán
        model_list = ["Naive Bayes", "Logistic Regression", "SVM", "K-Nearest Neighbors", "Decision Tree"]
        model_type = st.selectbox("🤖 Chọn Thuật toán Phân Loại", model_list)

        # Nút train model
        if st.button("🚀 Train Model"):
            classifier = TextClassifier(dataset_name, model_type)

            # 1️⃣ Hiển thị thanh tiến trình
            progress_bar = st.progress(0)
        
            # 2️⃣ Huấn luyện mô hình với progress bar cập nhật theo thời gian thực
            accuracy, train_time = classifier.train_model(progress_bar)

            # 3️⃣ Hiển thị kết quả
            st.success(f"✅ Mô hình '{model_type}' đạt độ chính xác: {accuracy * 100:.4f}%")
            st.write(f"⏳ Thời gian huấn luyện: {train_time:.4f} giây")

            # 4️⃣ Lưu mô hình vào session để sử dụng khi test
            st.session_state["classifier"] = classifier

        # Dự đoán văn bản mới
        st.markdown("### 📝 Dự đoán Văn Bản Mới")
        user_input = st.text_area("Nhập văn bản cần phân loại", "")

        if st.button("🎯 Dự đoán"):
            if "classifier" in st.session_state:
                classifier = st.session_state["classifier"]
                prediction = classifier.predict(user_input)
                st.info(f"📌 **Dự đoán:** {prediction}")
            else:
                st.warning("⚠️ Vui lòng train mô hình trước khi dự đoán!")
    with tab2:
        st.markdown(
            """
            ### 📌 Hướng dẫn sử dụng 
            - **Chọn Dataset**: Bạn có thể chọn dataset từ danh sách để huấn luyện mô hình.
            - **Chọn Thuật toán**: Chọn thuật toán phân loại mà bạn muốn sử dụng.
            - **Train Model**: Nhấn nút để bắt đầu huấn luyện mô hình.
            - **Dự đoán Văn bản Mới**: Nhập văn bản cần phân loại và nhấn nút "Dự đoán".
            """
        )