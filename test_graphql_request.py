import ast

import requests
import json

graphql_url = 'http://0.0.0.0:8000/graphql/'

model_query = """
           {{
               fmuModels(modelN: "{0}"){{
                    modelName
                }}
           }}
           """.format('xx')

r = requests.get(url=graphql_url, json={'query': model_query})

print(r.text)

d = r.json()['data']['fmuModels'][1]['modelName']
print(type(d))
"""
g = json.loads(json.loads(d))

print(g['time_step'])
print(g['yShadeFMU'])
print(g)
print(type(g))
"""