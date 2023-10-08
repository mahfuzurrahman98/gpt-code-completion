import requests
import json

url = 'http://127.0.0.1:8000/review-code'

response = requests.get(
    url,
    stream=True,
    headers={"accept": "application/json"},
)

print(response)

# if response.status_code == 200:
#     for chunk in response.iter_content(chunk_size=1024):
#         if chunk:
#             print(chunk.decode('utf-8'))  # Assuming the response is in UTF-8 encoding
# else:
#     print(f"Request failed with status code: {response.status_code}")