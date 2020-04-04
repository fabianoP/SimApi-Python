import requests


user_url = 'http://0.0.0.0:8000/user/'

user_email = 'user@user.com'
user_name = 'user'
user_password = 'user user88'

json = {
    "name": user_name,
    "email": user_email,
    "password": user_password
}

resp = requests.post(user_url, data=json)

print(resp.status_code)
print(resp.text)
