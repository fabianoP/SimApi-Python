import requests
import random
import time
import json

user_url = 'http://0.0.0.0:8000/user/'
login_url = 'http://0.0.0.0:8000/login/'
init_url = 'http://0.0.0.0:8000/init_model/'
input_url = 'http://0.0.0.0:8000/input/'
output_url = 'http://0.0.0.0:8000/output/'

# login details for super user
data = {"username": "user@user.com",  # username = email
        "password": "user user88"}

resp = requests.post(login_url, data=data)

# prints login token
print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header
i = 0   # first step
shade = 1.0  # input value. Stays same on each iteration. Will change on next update

# run 24 hour (86400sec) simulation at 10 minute (600sec) time steps
while i < 86400:
    # Actual inputs for simulation object. Stores as json in db
    input_dict = {'time_step': i, 'yShadeFMU': shade}

    input_data = {
        'fmu_model': 'sim7',    # Change name each time script is run!
        'time_step': i,     # 0 to 86400
        'input': json.dumps(input_dict)     # dumps input dict as json string to store in db
    }

    resp = requests.post(input_url, headers=header, data=input_data)

    # prints input_data on successful post
    print(resp.text)

    # increment time_step
    i += 600

    # wait for 1 second to allow data to propagate through the system and simulation to process time step.
    # Will change next update
    time.sleep(1)


