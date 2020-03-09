from bottle import request, route, run, response

import os.path
import tasks
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from energy_plus_to_fmu import RunEnergyPlusToFMU
from simulator_client import SimulatorClient


@route('/upload', method='POST')
# upload from sim container.
def do_upload():
    upload = request.files
    save_path = '/home/fmu/code/energy/test/'

    for name, file in upload.iteritems():
        file.save(save_path)

    return "Found {0} files".format(len(upload))


@route('/fmu/<container>')
# check task status on sim container for upload. when finished call this from sim
def generate(container):
    directory = os.listdir('/home/fmu/code/energy/test/')

    if container + '.idf' in directory and container + '.epw' in directory:
        epw = '/home/fmu/code/energy/test/' + container + '.epw'
        idf = '/home/fmu/code/energy/test/' + container + '.idf'
    else:
        response.status = 400
        return 'No such files'  # re-add task to queue?

    result = tasks.gen_fmu.apply_async((idf, epw))
    result.get()

    if os.path.exists('/home/fmu/code/energy/test/' + container + '.fmu'):

        response.status = 200
        return 'FMU ready'  # re-add task to queue
    else:
        response.status = 400
        return 'FMU not ready'  # re-add task to queue


@route('/get_fmu/<name>', method='GET')
def get_fmu(name):
    print('IN GET FMU')
    resp = SimulatorClient.put_fmu(name)
    print('IN GET FMU AFTER POST_FMU')
    response.status = resp
    return 'Sent FMU'


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
