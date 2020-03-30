import ast

import requests
import json

graphql_url = 'http://0.0.0.0:8000/graphql/'

j = """
{
    inputs(modelN: "sim1", tStep: 0) {
        inputJson
    }
}
"""

r = requests.get(url=graphql_url, json={'query': j})
print(r.text)

d = r.json()['data']['inputs'][0]['inputJson']

g = json.loads(json.loads(d))

print(g['time_step'])
print(g['yShadeFMU'])
print(g)
print(type(g))
