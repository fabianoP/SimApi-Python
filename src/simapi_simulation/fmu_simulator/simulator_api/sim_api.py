from bottle import request, route, run, response

import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


@route('/model_input', method='POST')
def get_input():
    with open('/home/deb/code/store_incoming_json/inputs.json') as json_file:
        # TODO NEEDS TO BE REFACTORED

        data = json.load(json_file)

        data['inputs'].append(request.json)

        print('TEMP APPEND DATA IN GET_INPUT: ' + str(data))

    write_json(data, '/home/deb/code/store_incoming_json/inputs.json')
    # TODO return code


@route('/upload/<model_name>', method='POST')
def do_upload(model_name):
    upload = request.files
    save_path = '/home/deb/code/volume/' + model_name

    json_data = request.forms.pop('json')
    print("IN SIM UPLOAD TEST JSON " + json_data)
    try:
        os.mkdir(save_path)
    except OSError:
        print("Creation of the directory %s failed" % save_path)
    else:
        print("Successfully created the directory %s " % save_path)

    for name, file in upload.iteritems():
        file.save(save_path)

    if len(upload) == 2:
        j_dict = {'model_params': []}

        j_dict['model_params'].append(json_data)
        write_json(j_dict, save_path + '/model_params.json')
        response.status = 200
        return 'File upload success in sim container for model_name = {0}'.format(model_name)
    else:
        response.status = 400
        return 'Number of Files required = 2. Uploaded Files = {0}'.format(len(upload))


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
