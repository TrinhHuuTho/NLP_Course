import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec, FastText
import gensim.downloader as api
import spacy
from transformers import BertTokenizer, BertModel, RobertaTokenizer, RobertaModel, GPT2Tokenizer, GPT2Model
import torch


class DataRepresentation:
    def __init__(self, method="count"):
        """
        Khởi tạo vectorizer dựa trên phương pháp đã chọn.
        method:
            - "count" -> CountVectorizer
            - "onehot" -> One-hot encoding
            - "bagofngram" -> Bag of N-grams
            - "tfidf" -> TF-IDF
            - "word2vec" -> Word2Vec Embedding
            - "glove" -> GloVe Embedding (dùng spaCy)
            - "fasttext" -> FastText Embedding
            - "bert" -> BERT Embedding
            - "roberta" -> RoBERTa Embedding
        """
        self.method = method
        self.vectorizer = None
        self.word2vec_model = None
        self.fasttext_model = None
        self.nlp = None

    def fit_transform(self, texts):
        """Chọn phương pháp biểu diễn dữ liệu phù hợp và thực hiện biến đổi."""
        if not texts:
            return "⚠️ Không có dữ liệu để biểu diễn!"

        method_map = {
            "count": self._count_vectorizer,
            "onehot": self._onehot_encoding,
            "bagofngram": self._bag_of_ngram,
            "tfidf": self._tfidf_vectorizer,
            "word2vec": self._word2vec_embedding,
            "glove": self._glove_embedding,
            "fasttext": self._fasttext_embedding,
            "chatgpt": self._chatgpt_embedding,
            "bert": self._bert_embedding,
            "roberta": self._roberta_embedding
        }

        if self.method in method_map:
            return method_map[self.method](texts)
        else:
            return "❌ Phương thức không hợp lệ!"

    # ========== Biểu diễn truyền thống ==========
    def _count_vectorizer(self, texts):
        """Bag of Words sử dụng CountVectorizer."""
        self.vectorizer = CountVectorizer(binary=False)
        transformed = self.vectorizer.fit_transform(texts)
        return self._to_dataframe(transformed)

    def _onehot_encoding(self, texts):
        """One-hot encoding = CountVectorizer(binary=True)."""
        self.vectorizer = CountVectorizer(binary=True)
        transformed = self.vectorizer.fit_transform(texts)
        return self._to_dataframe(transformed)

    def _bag_of_ngram(self, texts):
        """Bag of N-grams (n=1,2)."""
        self.vectorizer = CountVectorizer(ngram_range=(1, 2))
        transformed = self.vectorizer.fit_transform(texts)
        return self._to_dataframe(transformed)

    def _tfidf_vectorizer(self, texts):
        """TF-IDF Vectorization."""
        self.vectorizer = TfidfVectorizer()
        transformed = self.vectorizer.fit_transform(texts)
        return self._to_dataframe(transformed)

    # ========== Biểu diễn Word Embeddings ==========
    def _word2vec_embedding(self, texts):
        """Word2Vec embedding."""
        tokenized_texts = [text.split() for text in texts]
        self.word2vec_model = Word2Vec(sentences=tokenized_texts, vector_size=100, window=5, min_count=1, workers=4)
        embeddings = [np.mean([self.word2vec_model.wv[word] for word in text if word in self.word2vec_model.wv]
                              or [np.zeros(100)], axis=0) for text in tokenized_texts]
        return self._to_dataframe(np.array(embeddings))

    def _glove_embedding(self, texts):
        """GloVe embedding dùng api."""
        self.nlp = api.load("glove-wiki-gigaword-100")
        embeddings = [np.mean([self.nlp.get_vector(word) for word in text.split() if word in self.nlp], axis=0) for text in texts]
        return self._to_dataframe(np.array(embeddings))

    def _fasttext_embedding(self, texts):
        """FastText embedding."""
        tokenized_texts = [text.split() for text in texts]
        self.fasttext_model = FastText(sentences=tokenized_texts, vector_size=100, window=5, min_count=1, workers=4)
        embeddings = [np.mean([self.fasttext_model.wv[word] for word in text if word in self.fasttext_model.wv]
                              or [np.zeros(100)], axis=0) for text in tokenized_texts]
        return self._to_dataframe(np.array(embeddings))
    
    

    # ========== Biểu diễn BERT và RoBERTa ==========
    def _bert_embedding(self, texts):
        """Biểu diễn văn bản bằng BERT."""
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        model = BertModel.from_pretrained("bert-base-uncased")
        return self._transform_transformer(texts, tokenizer, model)

    def _roberta_embedding(self, texts):
        """Biểu diễn văn bản bằng RoBERTa."""
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        model = RobertaModel.from_pretrained("roberta-base")
        return self._transform_transformer(texts, tokenizer, model)
    

    # ========== Biểu diễn GPT-2 ==========
    def _chatgpt_embedding(self, texts):
        """Biểu diễn văn bản bằng GPT-2."""
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2Model.from_pretrained("gpt2")
        return self._transform_transformer(texts, tokenizer, model)
    
    
    # ========== Hàm chung cho các Transformer models ==========
    def _transform_transformer(self, texts, tokenizer, model):
        """Chuyển đổi văn bản sang embeddings từ Transformer models (BERT, RoBERTa)."""
        tokens = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
        return self._to_dataframe(embeddings)
    

    # ========== Chuyển đổi dữ liệu thành DataFrame ==========
    def _to_dataframe(self, transformed):
        """Chuyển ma trận thành DataFrame."""
        if len(transformed.shape) == 1:
            transformed = transformed.reshape(-1, 1)
        if isinstance(transformed, np.ndarray):
            return pd.DataFrame(transformed, columns=[f"Feature_{i+1}" for i in range(transformed.shape[1])])
        else:
            return pd.DataFrame(transformed.toarray(), columns=[f"Feature_{i+1}" for i in range(transformed.shape[1])])
