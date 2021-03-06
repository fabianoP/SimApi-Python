import sys

import polling2
import requests
import json

"""
This script provides the logic needed to run a simulation or multiple simulations.

initial_model_name: Needs to be same as model_name in initialize_model.py 
"""

initial_model_name = sys.argv[1]


user_url = 'http://0.0.0.0:8000/user/'
login_url = 'http://0.0.0.0:8000/login/'
init_url = 'http://0.0.0.0:8000/init_model/'
input_url = 'http://0.0.0.0:8000/input/'
output_url = 'http://0.0.0.0:8000/output/'
graphql_url = 'http://0.0.0.0:8000/graphql/'

# login details for super user
data = {"username": "user@user.com",  # username = email
        "password": "user user88"}

resp = requests.post(login_url, data=data)

# prints login token
print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header

# query for all models in db related to initial_model_name.
model_query = """
           {{
               fmuModels(modelN: "{0}"){{
                    modelName
                }}
           }}
           """.format(initial_model_name)

r = requests.get(url=graphql_url, json={'query': model_query})

i = 0
sim_names = []
number_of_sims = len(r.json()['data']['fmuModels'])
while i < number_of_sims:
    name = r.json()['data']['fmuModels'][i]['modelName']  # extract model name from graphql query response
    sim_names.append(name)  # store extracted model name.
    i += 1


shade = 1.0  # input value. Stays same on each iteration.

# up to 25 concurrent models can receive as input val(shade). [shade] * 25 expands the list from 1 to 25.
input_list = [shade] * 25

print(sim_names)
print(number_of_sims)

i = 0  # first step
# run 24 hour (86400sec) simulation at 10 minute (600sec) time steps
while i < 86400:  # outer loop iterates over time steps

    j = 0
    while j < number_of_sims:  # inner loop iterates over models, posing input to a different model on each iteration.
        input_dict = {'time_step': i, 'yShadeFMU': input_list[j]}  # input is user defined, can be any number of inputs

        input_data = {
            'fmu_model': sim_names[j],
            'time_step': i,
            'input_json': json.dumps(input_dict)
        }

        r = requests.post(input_url, headers=header, data=input_data)
        print(r.text + ' ' + str(r.status_code))

        output_query = """
        {{
            outputs(modelN: "{0}", tStep: {1}) {{
                outputJson
            }}
        }}
        """.format(sim_names[j], i)

        print(output_query)

        # move outside loop and poll once for len() = n, where n is number of simulations!
        polling2.poll(
            lambda: len(requests.get(url=graphql_url, json={'query': output_query}).json()['data']['outputs']) == 1,
            step=0.1,
            poll_forever=True)

        json_output = requests.get(url=graphql_url, json={'query': output_query}).json()['data']['outputs']
        print('After Poll = Sim: {0} | Output: {1}'.format(sim_names[j], str(json_output)))
        print('\n')
        j += 1

    i += 600
