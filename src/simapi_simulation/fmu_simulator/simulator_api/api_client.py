import coreapi
import requests

# TODO implement api client here. Receive input, provide output.

# resp = requests.get('http://web:8000/')
# print(resp)
data1 = {"username": "test@test.com",
         "password": "hello world88"}

resp_2 = requests.post('http://127.0.0.1:8000/login/', data=data1)
print(resp_2.headers)
print(resp_2.cookies)
print(resp_2.content)

data = resp_2.json

print(data)

