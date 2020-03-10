import requests

url = 'http://0.0.0.0:8002/upload/model'

file = {'epw': ('a.epw', open('test_setup_files/a.epw', 'rb')),
        'idf': ('a.idf', open('test_setup_files/a.idf', 'rb'))}

r = requests.post(url, files=file)

print(r.status_code)
print(r.text)


url = 'http://0.0.0.0:8002/upload/model_one'

file = {'epw': ('b.epw', open('test_setup_files/b.epw', 'rb')),
        'idf': ('b.idf', open('test_setup_files/b.idf', 'rb'))}

r = requests.post(url, files=file)

print(r.status_code)
print(r.text)


url = 'http://0.0.0.0:8002/upload/model_two'

file = {'epw': ('c.epw', open('test_setup_files/c.epw', 'rb')),
        'idf': ('c.idf', open('test_setup_files/c.idf', 'rb'))}

r = requests.post(url, files=file)

print(r.status_code)
print(r.text)
