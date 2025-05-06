import json
import os
from datetime import datetime
import re
import unicodedata
from ftfy import fix_text

def decode_facebook_text(text):
    if not text:
        return ""
    
    try:
        # Thử decode với các encoding khác nhau
        encodings = ['utf-8', 'latin1', 'cp1252', 'utf-16']
        for encoding in encodings:
            try:
                # Thử decode và encode lại để kiểm tra
                decoded = text.encode(encoding).decode('utf-8')
                if all(ord(c) < 0x10000 for c in decoded):  # Kiểm tra xem có ký tự Unicode hợp lệ không
                    return decoded
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
        
        # Nếu không decode được, trả về text gốc
        return text
    except Exception:
        return text

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Sử dụng ftfy để sửa text
    text = fix_text(text)
    
    # Chuyển đổi text về dạng unicode normalized
    text = unicodedata.normalize('NFKC', text)
    
    # Loại bỏ các ký tự đặc biệt và emoji, nhưng giữ lại dấu tiếng Việt
    text = re.sub(r'[^\w\s\u00C0-\u1FFF\u2C00-\uD7FF]', '', text)
    
    # Loại bỏ khoảng trắng thừa
    text = ' '.join(text.split())
    
    # Loại bỏ các URL và đường dẫn
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Loại bỏ các tin nhắn hệ thống
    if any(phrase in text.lower() for phrase in [
        "đã gửi", "đã chia sẻ", "đã bày tỏ cảm xúc", "đã gỡ",
        "file đính kèm", "ảnh", "video", "sticker", "gif"
    ]):
        return ""
    
    return text

def is_valid_conversation(msg1, msg2):
    # Kiểm tra độ dài tin nhắn
    if len(msg1) < 3 or len(msg2) < 3:
        return False
    
    # Kiểm tra xem có phải là tin nhắn hợp lệ không
    if not all(c.isprintable() for c in msg1 + msg2):
        return False
    
    # Kiểm tra xem tin nhắn có quá dài không
    if len(msg1) > 200 or len(msg2) > 200:
        return False
    
    # Kiểm tra xem tin nhắn có chứa quá nhiều ký tự đặc biệt không
    special_chars = len(re.findall(r'[^\w\s\u00C0-\u1FFF\u2C00-\uD7FF]', msg1 + msg2))
    if special_chars > len(msg1 + msg2) * 0.3:  # Nếu hơn 30% là ký tự đặc biệt
        return False
    
    # Kiểm tra xem tin nhắn có chứa quá nhiều số không
    numbers = len(re.findall(r'\d', msg1 + msg2))
    if numbers > len(msg1 + msg2) * 0.3:  # Nếu hơn 30% là số
        return False
    
    return True

def process_messages(json_file):
    try:
        # Đọc file JSON với encoding utf-8-sig
        with open(json_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Tạo thư mục corpus nếu chưa tồn tại
        if not os.path.exists('vietnamese_corpus'):
            os.makedirs('vietnamese_corpus')
        
        # Tạo file conversations.yml
        with open('vietnamese_corpus/conversations.yml', 'w', encoding='utf-8') as f:
            f.write('categories:\n')
            f.write('- conversations\n')
            f.write('conversations:\n')
            
            # Xử lý từng tin nhắn
            messages = data.get('messages', [])
            for i in range(len(messages)-1):
                current_msg = messages[i]
                next_msg = messages[i+1]
                
                # Kiểm tra nếu cả hai tin nhắn đều có nội dung
                if current_msg.get('content') and next_msg.get('content'):
                    # Làm sạch nội dung tin nhắn
                    current_content = clean_text(current_msg['content'])
                    next_content = clean_text(next_msg['content'])
                    
                    # Chỉ thêm vào corpus nếu cả hai tin nhắn đều hợp lệ
                    if current_content and next_content and is_valid_conversation(current_content, next_content):
                        f.write(f'- - "{current_content}"\n')
                        f.write(f'  - "{next_content}"\n')
        
        print(f"Đã xử lý xong file {json_file}")
        
    except Exception as e:
        print(f"Lỗi khi xử lý file {json_file}: {str(e)}")

def main():
    # Xử lý tất cả các file JSON trong thư mục hiện tại
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        print("Không tìm thấy file JSON nào trong thư mục hiện tại!")
        return
    
    for file in json_files:
        print(f'Đang xử lý file: {file}')
        process_messages(file)
    
    print('Đã xử lý xong tất cả các file JSON!')

if __name__ == "__main__":
    main() 