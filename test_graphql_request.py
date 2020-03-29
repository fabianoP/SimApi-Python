import requests
import json

graphql_url = 'http://0.0.0.0:8000/graphql/'

j = """
{
    inputs(modelN: "sim1") {
        inputJson
    }
}
"""

r = requests.get(url=graphql_url, json={'query': j})
print(r.text)

j = """
{
    outputs(modelN: "sim56", tStep: 600) {
        outputJson
    }
}
"""

r = requests.get(url=graphql_url, json={'query': j})
print(r.status_code)
print(r.text)

print(r.json())

print(type(r.json()))
print(len(r.json()['data']['outputs']))
out_dict = {'output': []}

for d in r.json()['data']['outputs']:
    #  print(json.loads(d['outputJson']))
    out_dict['output'].append(json.loads(d['outputJson']))

with open('outputs.json', 'w') as f:
    json.dump(out_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
