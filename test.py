import requests
import json

base_url = "http://development.localhost:8000"  # base URL of your API

url = "/api/method/login"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

data = {
    'usr': 'Administrator',
    'pwd': 'admin',
}

response = requests.post(base_url + url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}, {response.text}")
