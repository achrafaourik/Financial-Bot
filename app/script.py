import requests
import json

print('start')

user_payload = {
  "email": "user@example.com",
  "password": "string",
  "name": "user_test"
}

r = requests.post('http://localhost:8000/api/user/create/', json=user_payload)
res = json.loads(r.text)

print(res)
