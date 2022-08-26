import requests
import json

# create account
requests.post('http://localhost:8000/api/user/create/', json={'email': 'user@example.com', 'password': 'pass12345', 'name': 'test123'})

# generate token for the account
r = requests.post('http://localhost:8000/api/user/token/', json={'email': 'user@example.com', 'password': 'pass12345'})
token = json.loads(r.text)['token']

# create a savings account
data = {"account_type": "savings", "account_balance": 0}
r = requests.post('http://localhost:8000/api/banking/accounts/', json=data, headers={'Authorization': 'Token ' + token})
