import requests

url = "http://localhost:8008/model"
client = {"job": "management", "duration": 400, "poutcome": "success"}
res = requests.post(url, json=client).json()
print(res)