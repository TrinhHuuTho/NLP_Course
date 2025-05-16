import requests

BASE_URL = "https://tavusapi.com/v2/conversations"

def get_conversation(conversation_id, api_key):
    url = f"{BASE_URL}/{conversation_id}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy thông tin cuộc trò chuyện: {str(e)}")
        return None

def create_conversation(api_key, replica_id="rb17cf590e15", persona_id="p332c0870100"):
    """Tạo mới một cuộc trò chuyện Tavus."""
    url = BASE_URL
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = {
        "replica_id": replica_id,
        "persona_id": persona_id
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tạo cuộc trò chuyện: {str(e)}")
        return None

def end_conversation(conversation_id, api_key):
    url = f"{BASE_URL}/{conversation_id}/end"
    headers = {"x-api-key": api_key}
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        # Kiểm tra nếu response có nội dung trước khi parse JSON
        if response.text:
            return response.json()
        return {"status": "success", "message": "Cuộc trò chuyện đã được kết thúc"}
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi kết thúc cuộc trò chuyện: {str(e)}")
        return None