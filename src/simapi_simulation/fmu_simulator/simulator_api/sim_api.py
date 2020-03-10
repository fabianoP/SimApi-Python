from bottle import request, route, run, response

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject
from simulator_api.generator_client import GeneratorClient


@route('/init_model', method='POST')
# two separate uploads, one for files, one for json
def get_model_params():
    model_params = request.json


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
        resp = GeneratorClient.post_files(model_name)
    else:
        response.status = 400
        return 'Number of Files required = 2. Uploaded Files = {0}'.format(len(upload))

    if resp == 200:
        resp = GeneratorClient.gen_fmu(model_name)

    response.status = resp
    return 'Success'


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
