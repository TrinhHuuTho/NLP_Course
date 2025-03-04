import spacy
import nltk
import contractions
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.stem import PorterStemmer, SnowballStemmer
from spellchecker import SpellChecker
from spacy import displacy

# Tải mô hình ngôn ngữ English
nltk.download('punkt')

class TextPreprocessor:
    def __init__(self, text):
        """Khởi tạo lớp với văn bản đầu vào"""
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")  # Mô hình NLP của SpaCy
        self.spell = SpellChecker()  # Bộ kiểm tra lỗi chính tả
        self.doc = self.nlp(self.text)  # Phân tích văn bản với SpaCy
        self.stemmer = PorterStemmer()
        self.snowball = SnowballStemmer(language="english")

    def sentence_tokenization(self):
        """Tách câu"""
        return [sent.text for sent in self.doc.sents]

    def word_tokenization(self):
        """Tách từ"""
        return [token.text for token in self.doc]

    def remove_stopwords_punctuation(self):
        """Xóa stop words và dấu câu"""
        return [token.text for token in self.doc if not token.is_stop and not token.is_punct]

    def to_lowercase(self):
        """Viết thường tất cả từ"""
        return self.text.lower()

    def stemming(self, method="snowball"):
        """Áp dụng stemming (Porter hoặc Snowball)"""
        stem_func = self.snowball.stem
        return [stem_func(token.text) for token in self.doc]

    def lemmatization(self):
        """Đưa từ về dạng gốc"""
        return [(token.text, token.lemma_) for token in self.doc]

    def pos_tagging(self):
        """Xác định từ loại (POS tagging)"""
        return [(token.text, token.pos_) for token in self.doc]

    def expand_contractions(self):
        """Sửa lại các từ viết tắt"""
        return contractions.fix(self.text)

    def correct_spelling(self):
        """Sửa lỗi chính tả"""
        words = self.text.split()
        return " ".join([self.spell.correction(word) if self.spell.correction(word) else word for word in words])

    def named_entity_recognition(self):
        """Nhận diện thực thể (NER)"""
        return [(entity.text, entity.label_) for entity in self.doc.ents]

    def visualize_entities(self):
        """Hiển thị NER bằng HTML để Streamlit hiển thị"""
        html = displacy.render(self.doc, style="ent", page=True)
        return html  # Trả về HTML để hiển thị trong Streamlit
    
    def summary(self):
        """Tóm tắt tất cả các bước xử lý"""
        print("📌 **Sentence Tokenization:**", self.sentence_tokenization(), "\n")
        print("📌 **Word Tokenization:**", self.word_tokenization(), "\n")
        print("📌 **Remove Stopwords & Punctuation:**", self.remove_stopwords_punctuation(), "\n")
        print("📌 **Lowercase Text:**", self.to_lowercase(), "\n")
        print("📌 **Stemming (Porter):**", self.stemming("porter"), "\n")
        print("📌 **Lemmatization:**", self.lemmatization(), "\n")
        print("📌 **POS Tagging:**", self.pos_tagging(), "\n")
        print("📌 **Expand Contractions:**", self.expand_contractions(), "\n")
        print("📌 **Correct Spelling:**", self.correct_spelling(), "\n")
        print("📌 **Named Entities:**", self.named_entity_recognition(), "\n")
