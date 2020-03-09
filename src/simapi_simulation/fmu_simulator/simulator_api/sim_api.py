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


@route('/upload', method='POST')
def do_upload():
    upload = request.files
    save_path = '/home/deb/code/volume'

    for name, file in upload.iteritems():
        file.save(save_path)

    """Do if len(upload) == 2 post_files elif len 1 start sim else error handling"""
    if len(upload) == 2:
        resp = GeneratorClient.post_files()
    elif len(upload) == 1:
        response.status = 200
        return "Found {0} files".format(len(upload))
    else:
        response.status = 400
        return 'No files uploaded to sim_api/upload'

    if resp == 201 or resp == 200:
        resp = GeneratorClient.gen_fmu()

    if resp == 200:
        resp = GeneratorClient.get_fmu()

    response.status = resp
    return 'Success'


@route('/test', method='POST')
def test():
    upload = request.files
    print('IN TEST AFTER UPLOAD')
    save_path = '/home/deb/code/volume'

    for name, file in upload.iteritems():
        print('IN ITERITEMS TEST')
        file.save(save_path)

    if len(upload) == 1:
        response.status = 200
        return "Found {0} files".format(len(upload))
    else:
        response.status = 400
        return 'No files uploaded to sim_api/upload'


@route('/test_get_fmu')
def test():
    resp = GeneratorClient.get_fmu()
    response.status = resp
    return 'test_get_fmu success'


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
