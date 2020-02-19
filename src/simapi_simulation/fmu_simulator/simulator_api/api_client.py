import coreapi
import requests

# TODO implement api client here. Receive input, provide output.

#resp = requests.get('http://web:8000/')
#print(resp)

resp_2 = requests.get('http://web:8000/')
print(resp_2)

# client = coreapi.Client()
# scheme = client.get('http://web:8000/')

# action = ['login', 'post']

# params = {"username": "test@test.com", "password": "hello world88"}

# result = client.action(scheme, action, params)

# auth = coreapi.auth.TokenAuthentication(
#    scheme='JWT',
#    token=result['token']
# )
# client = coreapi.Client(auth=auth)

# new_init = client.action(scheme, ['init_model', 'create'], params={"model_name": "simulator",
#                                                                   "step_size": "600",
#                                                                  "final_time": "72.0"})
# print(new_init)
