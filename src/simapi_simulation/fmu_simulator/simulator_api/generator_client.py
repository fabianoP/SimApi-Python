import requests
import os


class GeneratorClient:

    @staticmethod
    def post_files(model_name):
        print("GEN CLIENT TRIGGERED")
        url = "http://generator:8000/upload/" + model_name

        directory = os.listdir('/home/deb/code/volume/' + model_name)

        simulator_idf = None
        simulator_epw = None

        for file in directory:
            if file.endswith('.idf'):
                simulator_idf = open('/home/deb/code/volume/' + model_name + '/' + file, 'rb')
            elif file.endswith('.epw'):
                simulator_epw = open('/home/deb/code/volume/' + model_name + '/' + file, 'rb')

        if simulator_idf is None or simulator_epw is None:
            return 405

        files = {'epw': (model_name+'.epw', simulator_epw),
                 'idf': (model_name+'.idf', simulator_idf)}

        r = requests.post(url, files=files)
        print("G CLIENT GEN /UPLOAD STATUS: " + str(r.status_code))

        simulator_epw.close()
        simulator_idf.close()
        # TODO FMU confirmation system needed
        if r.status_code == 200:
            url = "http://generator:8000/fmu/" + model_name
            print("G CLIENT GEN /FMU : " + str(r.status_code))
            r = requests.get(url)
            print(r.text)
            return r.status_code
        else:
            return 400

