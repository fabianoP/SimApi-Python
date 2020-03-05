import requests

# TODO implement api client here. Receive input, provide output.


"""
user_url = 'http://127.0.0.1:8000/user/'
login_url = 'http://127.0.0.1:8000/login/'
init_url = 'http://127.0.0.1:8000/init_model/'
input_url = 'http://127.0.0.1:8000/input/'
output_url = 'http://127.0.0.1:8000/output/'
user_url = 'http://web:8000/user/'
login_url = 'http://web:8000/login/'
init_url = 'http://web:8000/init_model/'
input_url = 'http://web:8000/input/'
output_url = 'http://web:8000/output/'
"""


user_url = 'http://127.0.0.1:8000/user/'
login_url = 'http://127.0.0.1:8000/login/'
init_url = 'http://127.0.0.1:8000/init_model/'
input_url = 'http://127.0.0.1:8000/input/'
output_url = 'http://127.0.0.1:8000/output/'

data = {"username": "test@test.com",
        "password": "hello world88"}

resp = requests.post(login_url, data=data)

print(resp.content)

json = resp.json()

"""
data = {"username": "test@test.com",
        "password": "hello world88"}

resp = requests.post(login_url, data=data)
json = resp.json()

token = json['token']
header = {'Authorization':  'Token ' + token}

input_data = {
  "fmu_model": "test1",
  "time_step": "600",
  "yshade": "2.0"
}

resp = requests.post(input_url, headers=header, data=input_data)

print(resp.text)


init_data = {"model_name": "test3",
             "step_size": "800",
             "final_time": "72.0"}

resp = requests.post(init_url, headers=header, data=init_data)

print(resp.text)

output_data = {
  "time_step": "800",
  "yshade": "2.4",
  "dry_bulb": "5.0",
  "troo": "7.0",
  "isolext": "4.01",
  "sout": "6.89",
  "zonesens": "9.111",
  "cool_rate": "18.9"
}

resp = requests.post(output_url, headers=header, data=output_data)

print(resp.text)
"""
