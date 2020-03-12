import requests


login_url = 'http://127.0.0.1:8000/login/'
init_url = 'http://127.0.0.1:8000/init_model/'


# replace with your superuser
data = {"username": "test@test.com",  # username = email
        "password": "test user88"}

resp = requests.post(login_url, data=data)

print(resp.content)

json = resp.json()

token = json['token']  # get validation token
header = {'Authorization':  'Token ' + token}  # set request header

file = {'idf_file': ('abdfgffdfhadaf.idf', open('test_setup_files/a.idf', 'rb')),
        'epw_file': ('afdhfsdgsfdaa.epw', open('test_setup_files/a.epw', 'rb'))}

init_data = {"model_name": "work17",
             "step_size": 600,
             "final_time": 72.0}

resp = requests.post(init_url, headers=header, data=init_data, files=file)

print(resp.text)


