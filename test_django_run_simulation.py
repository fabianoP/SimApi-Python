import polling2
import requests
import json

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


sim_names = ['xyz']

model_query = """
           {{
               fmuModels(modelN: "{0}"){{
                    modelName
                }}
           }}
           """.format(sim_names[0])

r = requests.get(url=graphql_url, json={'query': model_query})
i = 1
while i < 3:
    name = r.json()['data']['fmuModels'][i]['modelName']
    sim_names.append(name)
    i += 1

i = 0  # first step
shade = 2.0  # input value. Stays same on each iteration. Will change on next update
shade_1 = 3.0
shade_2 = 4.0
input_list = [shade, shade_1, shade_2]
# run 24 hour (86400sec) simulation at 10 minute (600sec) time steps
while i < 86400:

    j = 0
    while j < 3:
        input_dict = {'time_step': i, 'yShadeFMU': input_list[j]}

        input_data = {
            'fmu_model': sim_names[j],
            'time_step': i,
            'input_json': json.dumps(input_dict)
        }

        r = requests.post(input_url, headers=header, data=input_data)
        print(r.text)
        print('\n')
        output_query = """
        {{
            outputs(modelN: "{0}", tStep: {1}) {{
                outputJson
            }}
        }}
        """.format(sim_names[j], i)

        polling2.poll(
            lambda: len(requests.get(url=graphql_url, json={'query': output_query}).json()['data']['outputs']) == 1,
            step=0.1,
            poll_forever=True)

        json_output = requests.get(url=graphql_url, json={'query': output_query}).json()['data']['outputs']

        print('Sim: {0} | Output: {1}'.format(sim_names[j], str(json_output)))
        j += 1

    i += 600
