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
        response.status = 200
        return "Success"
    else:
        response.status = 400
        return "Found {0} files. Expected 2".format(len(upload))


@route('/upload/<model_name>', method='POST')
# upload from sim container.
def do_upload(model_name):
    upload = request.files
    save_path = '/home/fmu/code/energy/test/' + model_name

    try:
        os.mkdir(save_path)
    except OSError:
        print("Creation of the directory %s failed" % save_path)
    else:
        print("Successfully created the directory %s " % save_path)

    if len(upload) == 2:
        for name, file in upload.iteritems():
            print("GEN API /UPLOAD FILE SAVE: " + name)
            file.save(save_path)
        response.status = 200
        return '2 files uploaded'
    else:
        response.status = 400
        return "Found {0} files. Expected 2".format(len(upload))


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
