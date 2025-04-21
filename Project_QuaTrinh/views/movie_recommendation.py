import streamlit as st
from controllers.recommender import MovieRecommender

def movie_recommendation_view():
    st.title("🎬 Hệ thống Gợi Ý Phim")
    st.markdown("Dữ liệu: [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)")

    metadata_path = "data/movies_metadata.csv"
    ratings_path = "data/ratings.csv"

    recommender = MovieRecommender(metadata_path, ratings_path)

    # ========= SHOW VIDEO DEMO =========
    st.markdown("## 📽️ Trailer Demo")
    selected_movie = st.text_input("Nhập tên phim bạn muốn xem trailer:", "The Matrix")
    if selected_movie:
        search_query = selected_movie.replace(" ", "+") + "+trailer"
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        st.markdown(f"[🔗 Tìm trailer trên YouTube]({youtube_url})")

    # ========= USER INPUT =========
    st.markdown("---")
    st.markdown("## 👤 Gợi ý theo người dùng")
    user_id = st.number_input("Nhập user ID (theo tập ratings.csv):", min_value=1, value=1, step=1)
    if st.button("🎯 Gợi ý phim theo người dùng"):
        with st.spinner("Đang huấn luyện mô hình..."):
            recommender.train_user_based()
        recommendations = recommender.recommend_user_based(user_id)
        st.success("✅ Gợi ý thành công!")
        for _, row in recommendations.iterrows():
            st.write(f"📌 **{row['title']}**")
            st.caption(row['overview'])

    # ========= CONTENT BASED =========
    st.markdown("---")
    st.markdown("## 🧠 Gợi ý theo nội dung phim")
    if st.button("🚀 Huấn luyện Content-Based Model"):
        with st.spinner("Đang xử lý nội dung phim..."):
            recommender.preprocess_content()
        st.success("✅ Huấn luyện thành công!")

    selected_title = st.text_input("Nhập tên phim bạn thích để được gợi ý tương tự:")
    if selected_title:
        results = recommender.recommend_content_based(selected_title)
        if not results.empty:
            st.markdown("### 🎯 Danh sách phim tương tự:")
            for _, row in results.iterrows():
                st.write(f"📌 **{row['title']}**")
                st.caption(row['overview'])
        else:
            st.warning("⚠️ Không tìm thấy phim phù hợp!")

