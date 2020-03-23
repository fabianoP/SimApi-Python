import requests
import json

user_url = 'http://0.0.0.0:8000/user/'
login_url = 'http://0.0.0.0:8000/login/'
init_url = 'http://0.0.0.0:8000/init_model/'
input_url = 'http://0.0.0.0:8000/input/'
output_url = 'http://0.0.0.0:8000/output/'

# replace with your superuser
data = {"username": "user@user.com",  # username = email
        "password": "user user88"}

resp = requests.post(login_url, data=data)

print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header
i = 0
shade = 1.0

input_dict = {'time_step': i, 'yShadeFMU': shade}

input_data = {
    'fmu_model': 'nearly88',
    'input': json.dumps(input_dict)
}
resp = requests.post(input_url, headers=header, data=input_data)
print(resp.text)

"""
while i < 86400:

    input_dict = {'time_step': i, 'yShadeFMU': shade}

    input_data = {
        'fmu_model': 'nearly28',
        'input': json.dumps(input_dict)
    }

    resp = requests.post(input_url, headers=header, data=input_data)

    print(resp.text)

    i += 600
    shade += 0.1
    time.sleep(1)
"""

