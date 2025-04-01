import streamlit as st
import plotly.graph_objects as go
from controllers.data_classification import TextClassifier
import os
import pickle


def classification_view():
    tab1, tab2, tab3 = st.tabs(["Phân loại","Biểu đồ so sánh", "Hướng dẫn "])
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

        # Nếu chọn KNN, cho phép chọn số lượng lớp (chỉ số lẻ)
        if model_type == "K-Nearest Neighbors":
            n_neighbors = st.slider("🔢 Chọn số lượng lớp (k - chỉ số lẻ)", min_value=1, max_value=20, value=5, step=2)

        # Nút train model
        if st.button("🚀 Train Model"):
            if model_type == "K-Nearest Neighbors":
                classifier = TextClassifier(dataset_name, model_type, n_neighbors)
            else:
                classifier = TextClassifier(dataset_name, model_type, None)

            # 1️⃣ Hiển thị thanh tiến trình
            progress_bar = st.progress(0)
        
            # 2️⃣ Huấn luyện mô hình với progress bar cập nhật theo thời gian thực
            accuracy, train_time = classifier.train_model(progress_bar)

            # 3️⃣ Hiển thị kết quả
            st.success(f"✅ Mô hình '{model_type}' đạt độ chính xác: {accuracy * 100:.4f}%")
            st.write(f"⏳ Thời gian huấn luyện: {train_time:.4f} giây")

            # 4️⃣ Lưu mô hình vào session để sử dụng khi test
            if "comparison_data" not in st.session_state:
                st.session_state["comparison_data"] = {}

            if dataset_name not in st.session_state["comparison_data"]:
                st.session_state["comparison_data"][dataset_name] = {}

            st.session_state["comparison_data"][dataset_name][model_type] = {
                "accuracy": accuracy,
                "train_time": train_time
            }

        # Dự đoán văn bản mới
        st.markdown("### 📝 Dự đoán Văn Bản Mới")
        user_input = st.text_area("Nhập văn bản cần phân loại", "")

        if st.button("🎯 Dự đoán"):
            try:
                if model_type == "K-Nearest Neighbors":
                    classifier = TextClassifier(dataset_name, model_type, n_neighbors)
                else:
                    classifier = TextClassifier(dataset_name, model_type, None)
                prediction = classifier.predict([user_input])  # Cần truyền vào dạng list
                st.info(f"📌 **Dự đoán:** {prediction[0]}")
            except ValueError as e:
                st.error(str(e))

    with tab2:
        st.title("📊 Biểu đồ So Sánh")
        st.write("🔍 So sánh độ chính xác của các thuật toán phân loại trên các dataset khác nhau.")

        # Lấy danh sách dataset đã lưu từ các file trong thư mục 'pre-trained'
        saved_datasets = set()

        for model_folder in os.listdir("pre-trained"):
            model_path = os.path.join("pre-trained", model_folder)
            if os.path.isdir(model_path):  # Chỉ xét thư mục model
                for filename in os.listdir(model_path):
                    if filename.endswith(".pkl"):
                        dataset_name = "_".join(filename.split("_")[1:]).replace(".pkl", "")
                        saved_datasets.add(dataset_name)

        saved_datasets = list(saved_datasets)  # Chuyển thành danh sách để hiển thị

        # Giao diện chọn dataset để so sánh
        dataset_to_compare = st.selectbox("Chọn dataset để so sánh:", saved_datasets) if saved_datasets else None

        # Debug danh sách dataset lấy được
        print("DEBUG - Danh sách dataset lấy được:", saved_datasets)

        # Định nghĩa đường dẫn thư mục chứa model
        saved_models_path = "pre-trained"

        saved_models = []
        for model_folder in os.listdir(saved_models_path):
            model_path = os.path.join(saved_models_path, model_folder)
            if os.path.isdir(model_path):
                for filename in os.listdir(model_path):
                    if filename.endswith(".pkl"):
                        model_name = filename.split("_")[0]  # Lấy model type
                        dataset_name = "_".join(filename.split("_")[1:]).replace(".pkl", "")
                        if dataset_name == dataset_to_compare:
                            saved_models.append((model_name, dataset_name))

        if saved_models:
            # Tạo danh sách thuật toán & các chỉ số quan trọng để so sánh
            models = []
            train_times = []
            accuracies = []
            precision = []
            recall = []
            f1_score = []
            
            for model_type, dataset_name in saved_models:
                model_file = os.path.join(saved_models_path, model_type, f"{model_type}_{dataset_name}.pkl")

                print("DEBUG - Đường dẫn model_file:", repr(model_file))  # Debug đường dẫn

                with open(model_file, "rb") as f:
                    data = pickle.load(f)

                # Kiểm tra data có đúng 3 phần tử không
                if isinstance(data, tuple) and len(data) == 3:
                    model, vectorizer, model_data_dict = data
                else:
                    print(f"⚠️ File {model_file} không đúng định dạng, bỏ qua!")
                    continue  # Bỏ qua file lỗi

                print("DEBUG - model_data_dict:", repr(model_data_dict))  # Kiểm tra dữ liệu thực tế

                models.append(model_type)
                accuracies.append(model_data_dict["accuracy"])
                train_times.append(model_data_dict["train_time"])
                precision.append(model_data_dict["precision"])
                recall.append(model_data_dict["recall"])
                f1_score.append(model_data_dict["f1_score"])

            # Vẽ biểu đồ Accuracy & Train Time với hai trục y
            fig_acc_time = go.Figure()
            
            fig_acc_time.add_trace(go.Bar(
                x=models, y=accuracies, name="Accuracy", 
                text=[f"{a*100:.2f}%" for a in accuracies], textposition='auto',
                yaxis='y1'
            ))
            
            fig_acc_time.add_trace(go.Scatter(
                x=models, y=train_times, name="Train Time", 
                text=[f"{t:.2f}s" for t in train_times], textposition='top center',
                yaxis='y2', mode='lines+markers'
            ))
            
            fig_acc_time.update_layout(
                title=f"So sánh Accuracy & Train Time trên '{dataset_to_compare}'",
                xaxis_title="Thuật toán",
                yaxis=dict(title="Accuracy", side="left", showgrid=False),
                yaxis2=dict(title="Train Time (s)", overlaying='y', side='right', showgrid=False),
                template="plotly_white"
            )
            st.plotly_chart(fig_acc_time)

            # Vẽ Precision
            fig_precision = go.Figure([go.Bar(x=models, y=precision, text=[f"{p*100:.2f}%" for p in precision], textposition='auto')])
            fig_precision.update_layout(title="So sánh Precision", xaxis_title="Thuật toán", yaxis_title="Precision", template="plotly_white")
            st.plotly_chart(fig_precision)

            # Vẽ Recall
            fig_recall = go.Figure([go.Bar(x=models, y=recall, text=[f"{r*100:.2f}%" for r in recall], textposition='auto')])
            fig_recall.update_layout(title="So sánh Recall", xaxis_title="Thuật toán", yaxis_title="Recall", template="plotly_white")
            st.plotly_chart(fig_recall)

            # Vẽ F1-score
            fig_f1 = go.Figure([go.Bar(x=models, y=f1_score, text=[f"{f*100:.2f}%" for f in f1_score], textposition='auto')])
            fig_f1.update_layout(title="So sánh F1-score", xaxis_title="Thuật toán", yaxis_title="F1-score", template="plotly_white")
            st.plotly_chart(fig_f1)

        else:
            st.warning(f"⚠️ Không tìm thấy model nào cho dataset '{dataset_to_compare}'!")


    with tab3:
        st.markdown(
            """
            ### 📌 Hướng dẫn sử dụng 
            - **Chọn Dataset**: Bạn có thể chọn dataset từ danh sách để huấn luyện mô hình.
            - **Chọn Thuật toán**: Chọn thuật toán phân loại mà bạn muốn sử dụng.
            - **Train Model**: Nhấn nút để bắt đầu huấn luyện mô hình.    
                - **Lưu ý**: Hệ thống mặc định sử dụng **TF-IDF** để vector hóa dữ liệu với giới hạn **5000 từ vựng**. 
            Giảm thời gian huấn luyện, đồng thời độ chính xác cũng giảm. 
            Trên thực tế, có thể bỏ giới hạn từ vựng hoặc sử dụng vector hóa khác như Word2Vec, GloVe, BERT, ... 
            Nhưng cũng cần máy tính có cấu hình mạnh và thời gian huấn luyện cũng lâu hơn.
            - **Dự đoán Văn bản Mới**: Nhập văn bản cần phân loại và nhấn nút "Dự đoán".  
                - **Lưu ý**: Kết quả hiển thị chỉ số tương ứng với nhãn của dataset như sau:
                    - **IDMB Review**: Dùng để phân tích tình cảm của người dùng đối với phim. **(0: Tiêu cực, 1: Tích cực.)** 
                    - **Yelp Review**: Dùng để phân tích tình cảm của người dùng đối với nhà hàng. **(0: Tiêu cực, 1: Tích cực.)**  
                    - **Amazon Review**: Dùng để phân tích tình cảm của người dùng đối với sản phẩm. **(0: Tiêu cực, 1: Tích cực.)**
                    - **TREC**: Dùng để phân loại câu hỏi. 6 lớp: DESC, ENTY, ABBR, HUM, LOC, NUM. **(0 - 5.)** 
                    - **Yahoo! Answer**: Dùng để phân loại câu hỏi. 10 lớp: DESC, ENTY, ABBR, HUM, LOC, NUM, DESC, ENTY, ABBR, HUM. **(0 - 9.)** 
                    - **AG's News**: Dùng để phân loại tin tức. 4 lớp: World, Sports, Business, Sci/Tech. **(0 - 3.)**
                    - **Sogou News**: Dùng để phân loại tin tức. 5 lớp: Sports, Finance, Entertainment, Automobile, Technology. **(0 - 4.)**
                    - **DBPedia**: Dùng để phân loại Wikipedia. 14 lớp: Company, Educational Institution, Artist, Athlete, Office Holder, Mean of Transportation, Building, Natural Place, Village, Animal, Plant, Album, Film, Written Work. **(0 - 13.)**
            ---
            """
        )
        st.video("https://youtu.be/A4ZkI5JYRDA")
        st.caption("🎥 Hướng dẫn sử dụng Phân loại văn bản")