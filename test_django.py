import requests


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

file = {'idf_file': ('a.idf', open('test_setup_files/a.idf', 'rb')),
        'epw_file': ('a.epw', open('test_setup_files/a.epw', 'rb'))}

init_data = {'model_name': 'nearly88',
             'step_size': 600,
             'final_time': 24.0}

resp = requests.post(init_url, headers=header, data=init_data, files=file)

print(resp.text)
