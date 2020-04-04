import requests


user_url = 'http://0.0.0.0:8000/user/'
login_url = 'http://0.0.0.0:8000/login/'
init_url = 'http://0.0.0.0:8000/init_model/'
input_url = 'http://0.0.0.0:8000/input/'
output_url = 'http://0.0.0.0:8000/output/'

user_email = 'user@user.com'
user_name = 'user'
user_password = 'user user88'

json = {
    "name": user_name,
    "email": user_email,
    "password": user_password
}

resp = requests.post(user_url, data=json)
print(resp.text + ' ' + str(resp.status_code))

# login details for super user
data = {"username": "user@user.com",  # username = email
        "password": "user user88"}

resp = requests.post(login_url, data=data)

# prints login token
print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header

# place .idf and .epw in simapi-python/test_setup_files/  replace a.idf and a.epw
file = {'idf_file': ('update.idf', open('test_setup_files/update.idf', 'rb')),
        'epw_file': ('update.epw', open('test_setup_files/update.epw', 'rb'))}

# model initialization parameters
init_data = {
    'model_name': 'sim88',   # change name each time script is run!
    'container_id': None,
    'step_size': 600,   # step size in seconds. 600 secs = 10 mins
    'final_time': 24.0  # 24 hours = 86400 secs
}

resp = requests.post(init_url, headers=header, data=init_data, files=file)

# prints init_data on successful post
print(resp.text)
