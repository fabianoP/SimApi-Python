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
i = 0  # first step
shade = 2.0  # input value. Stays same on each iteration. Will change on next update

# run 24 hour (86400sec) simulation at 10 minute (600sec) time steps
while i < 86400:
    input_dict = {'time_step': i, 'yShadeFMU': shade}

    input_data = {
        'fmu_model': 'sim91',
        'time_step': i,
        'input_json': json.dumps(input_dict)
    }

    r = requests.post(input_url, headers=header, data=input_data)
    print(r.text)
    j = """
    {{
        outputs(modelN: "sim91", tStep: {0}) {{
            outputJson
        }}
    }}
    """.format(i)

    polling2.poll(
        lambda: len(requests.get(url=graphql_url, json={'query': j}).json()['data']['outputs']) == 1,
        step=0.1,
        poll_forever=True)

    print("grapghql output: " + str(requests.get(url=graphql_url, json={'query': j}).json()['data']['outputs']))
    i += 600
