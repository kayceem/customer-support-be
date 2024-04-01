# import requests


# def chatService(user_query):
#     api_url = "http://127.0.0.1:8001/api/Hrgpt/Rag/"

#     try:
#         payload = {"user_query": user_query}
#         response = requests.post(api_url, json=payload)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Error: {response.status_code} - {response.reason}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
