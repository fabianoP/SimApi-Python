from pathlib import Path

import requests
from bottle import request, route, run, response

import sys
import json
import os.path
import generator_tasks

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


@route('/test_upload/<model_name>', method='POST')
def test(model_name):
    upload = request.files
    save_path = '/home/fmu/code/energy/test/' + model_name
    json_data = request.forms.pop('json')
    print("json data: " + json_data)
    try:
        os.mkdir(save_path)
    except OSError:
        print("Creation of the directory %s failed" % save_path)
    else:
        print("Successfully created the directory %s " % save_path)

    if len(upload) == 2:
        for name, file in upload.iteritems():
            print("Saving: " + name)
            file.save(save_path)
    else:
        response.status = 400
        return "Found {0} files. Expected 2".format(len(upload))

    directory = os.listdir(save_path)
    print(directory)

    if model_name + '.idf' in directory and model_name + '.epw' in directory:
        epw = '/home/fmu/code/energy/test/' + model_name + '/' + model_name + '.epw'
        idf = '/home/fmu/code/energy/test/' + model_name + '/' + model_name + '.idf'
    else:
        response.status = 400
        return 'Error files not saved!'

    fmu_store_dir = '/home/fmu/code/fmu_test/' + model_name

    try:
        os.mkdir(fmu_store_dir)
    except OSError:
        print("Creation of the directory %s failed" % fmu_store_dir)
    else:
        print("Successfully created the directory %s " % fmu_store_dir)

    result = generator_tasks.gen_fmu.apply_async((idf, epw, fmu_store_dir))
    result.get()

    fmu_check = Path('/home/fmu/code/fmu_test/{0}/{0}.fmu'.format(model_name))
    fmu_zip_check = Path('/home/fmu/code/fmu_test/{0}/{0}.zip'.format(model_name))

    if fmu_check.exists():
        message = "FMU FILE EXISTS"
    elif fmu_zip_check.exists():
        message = "FMU ZIP EXISTS"
    else:
        message = "NO FMU OR ZIP"
        return message

    return message


@route('/fmu_to_simulator/<model_name>', method='POST')
def send_fmu(model_name):
    fmu_file = open('/home/fmu/code/fmu_test/' + model_name + '/' + model_name + '.fmu', 'rb')
    print(type(request.json))

    json_data = request.json

    model_count = json_data['model_count']
    print(model_count)

    i = 1
    while i <= int(model_count):
        file = {'fmu': (model_name + '.fmu', fmu_file, 'application/zip'),
                'json': (None, json.dumps(json_data), 'application/json')}

        url = 'http://src_simulator_{0}:8000/test_fmu/{1}'.format(i, model_name)

        r = requests.post(url, files=file)

        print(r.text)
        i += 1

    fmu_file.close()
    response.status = 200
    return 'File upload success in sim container for model_name = {0}'.format(model_name)


@route('/fmu/<model_name>')
# check task status on sim container for upload. when finished call this from sim
def generate(model_name):
    directory = os.listdir('/home/fmu/code/energy/test/' + model_name)

    # maybe write to .json file and monitor for updates
    if model_name + '.idf' in directory and model_name + '.epw' in directory:
        epw = '/home/fmu/code/energy/test/' + model_name + '/' + model_name + '.epw'
        idf = '/home/fmu/code/energy/test/' + model_name + '/' + model_name + '.idf'
    else:
        response.status = 400
        return 'No such files'

    fmu_store_dir = '/home/fmu/code/fmu_location/' + model_name

    try:
        os.mkdir(fmu_store_dir)
    except OSError:
        print("Creation of the directory %s failed" % fmu_store_dir)
    else:
        print("Successfully created the directory %s " % fmu_store_dir)

    # result = generator_tasks.gen_fmu.apply_async((idf, epw, fmu_store_dir))
    # result.get()

    if os.path.exists(fmu_store_dir):
        # write JSON file here '/home/fmu/code/energy/test/' + model_name + '/'
        # model_name, epw, idf, fmu_store_dir
        data = {'epw_path': epw,
                'idf_path': idf,
                'fmu_store_dir': fmu_store_dir}

        with open('/home/fmu/code/energy/test/' + model_name + '/data.json', 'w') as f:
            json.dump(data, f)
            f.close()

        response.status = 200
        return 'FMU ready'  # FMU Stored in shared volume
    else:
        response.status = 400
        return 'FMU not ready'  # re-add task to queue


run(host='0.0.0.0', port=8000, debug=True, reloader=True)
