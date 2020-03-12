from bottle import request, route, run, response

import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator_api.generator_client import GeneratorClient
import simulator_tasks

model = None
# model_task = simulator_tasks.ModelInitTask()


def write_json(data, filename):
    with open(filename, 'a+') as f:
        json.dump(data, f, indent=4)


@route('/set_model', method='POST')
def get_model_params():

    with open('../store_incoming_json/model_params.json') as json_file:
        data = json.load(json_file)

        temp = data['model_params']

        temp.append(request.json)

    write_json(data, '../store_incoming_json/model_params.json')

    # TODO Write to model_params.json, move task to json monitor


@route('/model_input', method='POST')
def get_input():
    with open('../store_incoming_json/inputs.json') as json_file:
        data = json.load(json_file)

        temp = data['inputs']

        temp.append(request.json)

    write_json(data, '../store_incoming_json/inputs.json')
    # TODO Write to inputs.json, move task to json monitor


@route('/upload/<model_name>', method='POST')
def do_upload(model_name):
    upload = request.files
    save_path = '/home/deb/code/volume/' + model_name

    try:
        os.mkdir(save_path)
    except OSError:
        print("Creation of the directory %s failed" % save_path)
    else:
        print("Successfully created the directory %s " % save_path)

    for name, file in upload.iteritems():
        file.save(save_path)

    if len(upload) == 2:
        # TODO move to volume_monitor.py resp = GeneratorClient.post_files(model_name)
        response.status = 200
        return 'File upload success in sim container for model_name = {0}'.format(model_name)
    else:
        response.status = 400
        return 'Number of Files required = 2. Uploaded Files = {0}'.format(len(upload))

    # if resp == 200:
    # TODO resp = GeneratorClient.gen_fmu(model_name)
    #  set up file monitor in generator and gen model
    #  there instead of here


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
