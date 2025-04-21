import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

class MovieRecommender:
    def __init__(self, metadata_path, ratings_path):
        self.movies = pd.read_csv(metadata_path, low_memory=False)
        self.ratings = pd.read_csv(ratings_path)
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.svd_model = None

    def preprocess_content(self):
        self.movies = self.movies.dropna(subset=["overview"])
        self.movies["overview"] = self.movies["overview"].fillna("")
        tfidf = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = tfidf.fit_transform(self.movies["overview"])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_content_based(self, title, top_n=5):
        indices = pd.Series(self.movies.index, index=self.movies["title"]).drop_duplicates()
        if title not in indices:
            return []
        idx = indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        movie_indices = [i[0] for i in sim_scores]
        return self.movies.iloc[movie_indices][["title", "overview"]]

    def train_user_based(self):
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(self.ratings[["userId", "movieId", "rating"]], reader)
        trainset, _ = train_test_split(data, test_size=0.2)
        self.svd_model = SVD()
        self.svd_model.fit(trainset)

    def recommend_user_based(self, user_id, top_n=5):
        user_movies = self.ratings[self.ratings["userId"] == user_id]["movieId"].tolist()
        all_movies = self.ratings["movieId"].unique()
        movies_to_predict = list(set(all_movies) - set(user_movies))
        predictions = [self.svd_model.predict(user_id, mid) for mid in movies_to_predict]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_ids = [pred.iid for pred in predictions[:top_n]]
        recommended = self.movies[self.movies["id"].astype(str).isin(map(str, top_ids))]
        return recommended[["title", "overview"]]
