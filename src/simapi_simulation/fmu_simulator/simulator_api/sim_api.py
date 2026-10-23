import subprocess

from bottle import request, route, run, response

import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_time_step(t_step, filename):
    with open(filename, 'w') as f:
        f.seek(0)
        f.write(t_step)


@route("/model_input", method="POST")
def get_input():
    data = request.json
    if not isinstance(data, dict) or "time_step" not in data:
        response.status = 400
        return "Expected a JSON object containing time_step"

    write_time_step(str(data["time_step"]), "/home/deb/code/store_incoming_json/time_step.txt")
    response.status = 204


@route('/upload/<model_name>', method='POST')
def do_upload(model_name):
    upload = request.files
    save_path = '/home/deb/code/volume/' + model_name
    print('UPLOAD SIM')
    with open('/home/deb/code/isSwarm.txt', 'w') as f:
        f.write("isSwarm?")
    
    json_data = request.forms.pop('json')
    
    try:
        os.mkdir(save_path)
    except OSError:
        print("Creation of the directory %s failed" % save_path)
    else:
        print("Successfully created the directory %s " % save_path)

    for name, file in upload.items():
        file.save(save_path)

    subprocess.getoutput('chmod -R  a+rw /home/deb/code/volume/ *')

    if len(upload) == 2:
        j_dict = {'model_params': []}

        j_dict['model_params'].append(json.loads(json_data))
        write_json(j_dict, save_path + '/model_params.json')
        response.status = 200
        return 'File upload success in sim container for model_name = {0}'.format(model_name)
    else:
        response.status = 400
        return 'Number of Files required = 2. Uploaded Files = {0}'.format(len(upload))


if __name__ == "__main__":
    run(host="0.0.0.0", port=8000, debug=False, reloader=False)
