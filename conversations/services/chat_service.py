import requests
from conversations.services.rag_service import RagService


def chatService(user_message):
    try:
        return RagService(user_message)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
