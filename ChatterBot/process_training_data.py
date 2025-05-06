import json
import yaml
import os
from process_messages import clean_text, is_valid_conversation

def convert_to_yaml_format(conversations):
    """Chuyển đổi dữ liệu hội thoại sang định dạng YAML cho ChatterBot"""
    yaml_data = {
        'categories': ['conversations'],
        'conversations': []
    }
    
    for conv in conversations:
        if len(conv) >= 2:  # Đảm bảo có ít nhất 2 tin nhắn trong cuộc hội thoại
            yaml_data['conversations'].append(conv)
    
    return yaml_data

def process_json_to_yaml(json_file):
    """Xử lý file JSON và chuyển đổi sang YAML"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                # Thử parse JSON nếu là chuỗi JSON
                data = json.loads(content)
            except json.JSONDecodeError:
                # Nếu không phải JSON, xử lý như text thông thường
                data = [{'type': 'message', 'text': line.strip()} 
                       for line in content.split('\n') 
                       if line.strip()]
        
        conversations = []
        current_conversation = []
        
        for message in data:
            if isinstance(message, dict) and message.get('type') == 'message':
                text = clean_text(message.get('text', ''))
            elif isinstance(message, str):
                text = clean_text(message)
            else:
                continue
                
            if text:
                current_conversation.append(text)
                
                # Nếu có đủ 2 tin nhắn, kiểm tra tính hợp lệ
                if len(current_conversation) == 2:
                    if is_valid_conversation(current_conversation[0], current_conversation[1]):
                        conversations.append(current_conversation.copy())
                    current_conversation = []
        
        # Chuyển đổi sang định dạng YAML
        yaml_data = convert_to_yaml_format(conversations)
        
        # Tạo thư mục vietnamese_corpus nếu chưa tồn tại
        os.makedirs('vietnamese_corpus', exist_ok=True)
        
        # Lưu file YAML
        output_file = os.path.join('vietnamese_corpus', 'conversations.yml')
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
            
        print(f"Đã xử lý và lưu {len(conversations)} cuộc hội thoại vào {output_file}")
        
    except Exception as e:
        print(f"Lỗi khi xử lý file {json_file}: {str(e)}")

def main():
    # Xử lý tất cả các file JSON trong thư mục hiện tại
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        print("Không tìm thấy file JSON nào trong thư mục hiện tại")
        return
        
    for json_file in json_files:
        print(f"Đang xử lý file: {json_file}")
        process_json_to_yaml(json_file)

if __name__ == "__main__":
    main() 