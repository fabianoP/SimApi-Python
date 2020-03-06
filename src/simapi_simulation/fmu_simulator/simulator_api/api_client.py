import requests

# TODO fmu generator should take .idf files with the fmu model_name the same as the db entry for init_model endpoint.
#  The name can then be used to retrieve input for that model,
#  this will be necessary when run in swarm mode.
#  Inputs should have datetime field so this api can retrieve the latest input for given model.
#  a list of each input can be stored to ensure that no inputs are skipped over by checking datetime i.e. memoization
#


"""
user_url = 'http://127.0.0.1:8000/user/'
login_url = 'http://127.0.0.1:8000/login/'
init_url = 'http://127.0.0.1:8000/init_model/'
input_url = 'http://127.0.0.1:8000/input/'
output_url = 'http://127.0.0.1:8000/output/'
"""

# web references name of API container no need for IP if containers are on the same network
user_url = 'http://web:8000/user/'
login_url = 'http://web:8000/login/'
init_url = 'http://web:8000/init_model/'
input_url = 'http://web:8000/input/'
output_url = 'http://web:8000/output/'

# replace with your superuser
data = {"username": "test@test.com",  # username = email
        "password": "hello world88"}

resp = requests.post(login_url, data=data)

print(resp.content)

json = resp.json()

token = json['token']  # get validation token
header = {'Authorization':  'Token ' + token}  # set request header


init_data = {"model_name": "test4",
             "step_size": "800",
             "final_time": "72.0"}

resp = requests.post(init_url, headers=header, data=init_data)

print(resp.text)

input_data = {
  "fmu_model": "test4",
  "time_step": "600",
  "yshade": "2.0"
}

resp = requests.post(input_url, headers=header, data=input_data)

print(resp.text)

output_data = {
  "fmu_model": "test4",
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


# TODO structure of simulator script
#  use celery to alert client to /init_model/
#  client queries /init_model/
#  sim_obj initialized celery wait for /input/
#  celery alert client when /input/
#  client queries /input/
#  call sim_obj.do_step
#  celery output to client
#  client sends output to API
#

