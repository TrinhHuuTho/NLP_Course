from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Tạo chatbot với cấu hình tiếng Việt
vietnamese_bot = ChatBot(
    "VietnameseBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Xin lỗi, tôi không hiểu ý bạn. Bạn có thể diễn đạt theo cách khác được không?',
            'maximum_similarity_threshold': 0.85
        },
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ]
)

# Train chatbot với corpus tiếng Việt
trainer = ChatterBotCorpusTrainer(vietnamese_bot)
print("Bắt đầu training chatbot...")
try:
    trainer.train("./vietnamese_corpus")
    print("Đã hoàn thành training!")
except Exception as e:
    print(f"Lỗi khi training: {str(e)}")

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
        response = vietnamese_bot.get_response(userText)
        return str(response)
    except Exception as e:
        print(f"Lỗi khi xử lý tin nhắn: {str(e)}")
        return "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau."

if __name__ == "__main__":
    app.run(debug=True)