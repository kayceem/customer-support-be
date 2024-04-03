import requests
from django.conf import settings


def chatService(user_message):
    api_url = settings.RAG_URL

    try:
        payload = {"user_message": user_message}
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
