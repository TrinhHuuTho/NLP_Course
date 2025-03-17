import streamlit as st

def Header():
    st.markdown(
        """
        <div style="text-align:center">
            <h1>🚀 NLP Project - Xử lý Ngôn ngữ Tự nhiên</h1>
            <p style="font-size:18px;">Chào mừng bạn đến với ứng dụng NLP! Đây là một dự án môn Xử lý Ngôn ngữ Tự nhiên.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.vega_lite_chart({
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A bar chart showing the distribution of NLP scores.",
        "data": {
            "values": [
                {"category": "Accuracy", "score": 0.85},
                {"category": "Precision", "score": 0.78},
                {"category": "Recall", "score": 0.82},
                {"category": "F1-Score", "score": 0.80}
            ]
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": "category", "type": "nominal", "title": "Metric"},
            "y": {"field": "score", "type": "quantitative", "title": "Score"},
            "color": {"field": "category", "type": "nominal"}
        }
    })

def Menu():
    st.sidebar.title("📌 Menu")
    menu = [
        "🏠 Trang chủ",
        "📝 Tăng cường dữ liệu",
        "📥 Thu thập dữ liệu",
        "🔍 Tiền xử lý dữ liệu",
        "🔢 Biểu diễn dữ liệu",
        "📚 Phân loại dữ liệu",
        "📞 Liên hệ"
    ]
    return st.sidebar.selectbox("🔽 Chọn chức năng", menu)

def Body():
    st.markdown("### 📌 Giới thiệu dự án NLP")
    st.write(
        "🚀 Dự án này giúp thực hiện các tác vụ NLP như tăng cường dữ liệu, thu thập dữ liệu, tiền xử lý, và trực quan hóa kết quả. "
        "Bằng cách sử dụng các mô hình học máy tiên tiến, bạn có thể khám phá cách xử lý ngôn ngữ một cách hiệu quả."
    )

    # Chia layout thành 2 phần
    col1, col2 = st.columns([1, 1])

    with col1:
        st.video("https://www.youtube.com/watch?v=CMrHM8a3hqw&ab_channel=Simplilearn")
        st.caption("🎯 Never give up!")

    with col2:
        st.subheader("✨ Các tính năng chính:")
        st.write("✅ **Tăng cường dữ liệu NLP** với Synonym, Swap, Insert, Delete, Back Translation...")
        st.write("✅ **Thu thập dữ liệu tự động** từ các nguồn web")
        st.write("✅ **Tiền xử lý dữ liệu** với loại bỏ stopwords, stemming, lemmatization...")
        st.write("✅ **Biểu diễn dữ liệu** ")
        

    # st.markdown("---")
    # st.subheader("📌 Bắt đầu ngay!")
    # col3, col4 = st.columns([1, 1])

    # with col3:
    #     if st.button("🔍 Khám phá tính năng NLP"):
    #         st.switch_page("Tăng cường dữ liệu")

    # with col4:
    #     if st.button("📊 Xem thống kê dữ liệu"):
    #         st.switch_page("Trực quan hóa dữ liệu")

def Footer():
    st.markdown("---")
    st.info("⚠️ Trang web hiện chỉ hỗ trợ xử lý trên ngôn ngữ Tiếng Anh.")

    st.markdown("### 📞 Thông tin liên hệ")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("📩 **Email:** trinhuutho@gmail.com")
        # st.write("🌐 **Website:** [nlp-project.com](https://nlp-project.com)")
        st.write("📌 **Facebook:** [Facebook Page](https://www.facebook.com/tho.trinh.56614)")
        # st.write("📌 **LinkedIn:** [LinkedIn Page](https://linkedin.com/in/nlp-project)")
    with col2:
        st.image("https://byvn.net/Il7R", width=200)
    st.markdown("---")

# Windows + . (dấu chấm) để mở bảng chọn icon