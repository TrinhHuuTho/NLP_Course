import streamlit as st
import pandas as pd
from controllers.data_representation import DataRepresentation

def representation_view():
    # 🎯 **Giao diện chính**
    tab1, tab2 = st.tabs(["Biểu diễn", "Hướng dẫn "])
    with tab1:
      st.title("🔢 Công cụ Biểu Diễn Văn Bản")
      st.write("Công cụ này giúp bạn chuyển đổi văn bản thành dạng vector sử dụng One-hot Encoding hoặc CountVectorizer.")

      # 📂 **Chọn loại input**
      input_type = st.radio("Chọn nguồn dữ liệu:", ("Nhập văn bản", "Tải file văn bản (.txt)"))

      # 📝 **Nhập văn bản hoặc tải file**
      text_data = []
      if input_type == "Nhập văn bản":
          input_text = st.text_area("Nhập văn bản của bạn (mỗi dòng là một mẫu dữ liệu):", height=200)
          text_data = input_text.split("\n") if input_text else []

      elif input_type == "Tải file văn bản (.txt)":
          uploaded_file = st.file_uploader("📂 Chọn file .txt", type="txt")
          if uploaded_file:
              text_data = uploaded_file.read().decode("utf-8").split("\n")

      # 📌 **Chọn phương pháp**
      method = st.radio("Chọn phương pháp biểu diễn:", ("One-hot Encoding",
                                                        "CountVectorizer",
                                                          "Bag of N-grams (n=1,2)",
                                                            "TF-IDF Vectorizer",
                                                              "Word2Vec Embedding",
                                                                "GloVe Embedding",
                                                                  "FastText Embedding",
                                                                    "ChatGPT Embedding",
                                                                      "BERT Embedding",
                                                                        "RoBERTa Embedding"))

      # ✅ **Nút xử lý**
      if st.button("🚀 Biểu diễn văn bản"):
          if text_data:
              vectorizer = DataRepresentation(method="count" if method == "CountVectorizer"
                                                      else "onehot" if method == "One-hot Encoding"
                                                      else "bagofngram" if method == "Bag of N-grams (n=1,2)"
                                                      else "tfidf" if method == "TF-IDF Vectorizer"
                                                      else "word2vec" if method == "Word2Vec Embedding"
                                                      else "glove" if method == "GloVe Embedding"
                                                      else "fasttext" if method == "FastText Embedding"
                                                      else "chatgpt" if method == "ChatGPT Embedding"
                                                      else "bert" if method == "BERT Embedding"
                                                      else "roberta" if method == "RoBERTa Embedding"
                                                      else "count")
              result = vectorizer.fit_transform(text_data)
              if not isinstance(result, pd.DataFrame):
                  result = pd.DataFrame(result)
              
              if isinstance(result, pd.DataFrame):
                  st.subheader("📊 Kết quả Biểu Diễn Dữ Liệu")
                  st.dataframe(result)
                  
                  # 💾 **Nút tải kết quả**
                  csv_data = result.to_csv(index=False).encode("utf-8")
                  st.download_button("💾 Tải kết quả CSV", data=csv_data, file_name="vectorized_data.csv", mime="text/csv")
              else:
                  st.warning(result)
          else:
              st.warning("⚠️ Vui lòng nhập dữ liệu!")
    with tab2:
        st.markdown(
            """
            ### 📌 Hướng dẫn sử dụng 
            - **Nhập văn bản**: Bạn có thể nhập văn bản trực tiếp vào ô văn bản hoặc tải file văn bản. Mỗi dòng là một mẫu dữ liệu.
            - **Chọn phương pháp**: Chọn phương pháp biểu diễn dữ liệu từ danh sách.
            - **Biểu diễn văn bản**: Nhấn nút để thực hiện biểu diễn dữ liệu.
            - **Kết quả**: Kết quả sẽ hiển thị ở bên dưới.
            - **Tải xuống**: Bạn có thể tải xuống kết quả biểu diễn dữ liệu bằng cách nhấn nút "Tải xuống".
            ---
            """
          )
        st.video("https://youtu.be/A4ZkI5JYRDA")
        st.caption("🎥 Hướng dẫn sử dụng Biểu diễn dữ liệu")
