import streamlit as st
from controllers.data_classification import TextClassifier

def classification_view():
    st.title("📚 Text Classification - Phân loại văn bản")

    # Chọn dataset
    dataset_list = [
        "SST", "IMDb Review", "Yelp Review", "Amazon Review", 
        "TREC", "Yahoo! Answer", "AG's News", "Sogou News", "DBPedia"
    ]
    dataset_name = st.selectbox("🗂 Chọn Dataset", dataset_list)

    # Chọn thuật toán
    model_list = ["Naive Bayes", "Logistic Regression", "SVM"]
    model_type = st.selectbox("🔍 Chọn Thuật toán Phân Loại", model_list)

    # Nút train model
    if st.button("🚀 Train Model"):
        classifier = TextClassifier(dataset_name, model_type)
        accuracy = classifier.train_model()
        st.success(f"✅ Mô hình '{model_type}' đạt độ chính xác: {accuracy:.4f}")

        # Lưu model vào session để sử dụng khi test
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
