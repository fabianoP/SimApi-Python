import requests

input_url = 'http://127.0.0.1:8000/input/'
login_url = 'http://127.0.0.1:8000/login/'

# replace with your superuser
data = {"username": "user@user.com",  # username = email
        "password": "user user88"}

resp = requests.post(login_url, data=data)

print(resp.content)

json = resp.json()

token = json['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header

input_data = {
    "fmu_model": "nearly10",
    "time_step": 0,
    "yshade": 3.0
}

resp = requests.post(input_url, headers=header, data=input_data)

print(resp.text)
