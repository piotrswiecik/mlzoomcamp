import requests

url = "http://localhost:8008/model"
client = {"job": "student", "duration": 280, "poutcome": "failure"}
res = requests.post(url, json=client).json()
print(res)