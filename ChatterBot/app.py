from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from functools import lru_cache
import yaml
import codecs

app = Flask(__name__)

# Khởi tạo model tiếng Việt
vietnamese_model = SentenceTransformer('keepitreal/vietnamese-sbert')

class VietnameseEmbeddingComparison:
    def __init__(self, model):
        self.model = model
        
    def compare(self, statement_a, statement_b):
        # Chuyển đổi câu thành vector
        embedding_a = self.model.encode(statement_a.text)
        embedding_b = self.model.encode(statement_b.text)
        
        # Tính cosine similarity
        similarity = np.dot(embedding_a, embedding_b) / (np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b))
        return similarity

# Tạo chatbot với cấu hình tiếng Việt
vietnamese_bot = ChatBot(
    "VietnameseBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Xin lỗi, tôi không hiểu ý bạn. Bạn có thể diễn đạt theo cách khác được không?',
            'maximum_similarity_threshold': 0.85,
            'statement_comparison': VietnameseEmbeddingComparison(vietnamese_model),
            'response_selection': get_first_response
        },
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///vietnamese_bot.db'
)

# Train chatbot với corpus tiếng Việt
trainer = ChatterBotCorpusTrainer(vietnamese_bot)
print("Bắt đầu training chatbot...")
try:
    # Training trực tiếp từ các file corpus
    trainer.train("./vietnamese_corpus/ai.yml")
    print("Đã hoàn thành training chủ đề AI!")

    trainer.train("./vietnamese_corpus/casual_conversation.yml")
    print("Đã hoàn thành training chủ đề Casual Conversations!")

    trainer.train("./vietnamese_corpus/conversations.yml")
    print("Đã hoàn thành training chủ đề Conversations!")

    trainer.train("./vietnamese_corpus/daily_life.yml")
    print("Đã hoàn thành training chủ đề Daily Life!")

    trainer.train("./vietnamese_corpus/ethics_and_future.yml")
    print("Đã hoàn thành training chủ đề Ethics and Future!")

    trainer.train("./vietnamese_corpus/tech_support.yml")
    print("Đã hoàn thành training chủ đề Tech Support!")

    trainer.train("./vietnamese_corpus/technology.yml")
    print("Đã hoàn thành training chủ đề Technology!")
    
except Exception as e:
    print(f"Lỗi khi training: {str(e)}")
    import traceback
    print(traceback.format_exc())

# Cache cho các câu trả lời thường gặp
@lru_cache(maxsize=1000)
def get_cached_response(user_text):
    return str(vietnamese_bot.get_response(user_text))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not userText:
        return "Xin lỗi, tôi không hiểu ý bạn."
    try:
        # Làm sạch dữ liệu đầu vào
        userText = ' '.join(str(userText).split())
        # Sử dụng cache
        response = get_cached_response(userText)
        return response
    except Exception as e:
        print(f"Lỗi khi xử lý tin nhắn: {str(e)}")
        return "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau."

if __name__ == "__main__":
    app.run(debug=True)