import requests


class GeneratorClient:

    @staticmethod
    def post_files():
        url = "http://generator:8000/upload"

        simulator_epw = open('/home/deb/code/volume/simulator.epw', 'rb')
        simulator_idf = open('/home/deb/code/volume/simulator.idf', 'rb')

        files = {'epw': ('simulator.epw', simulator_epw),
                 'idf': ('simulator.idf', simulator_idf)}

        r = requests.post(url, files=files)

        simulator_epw.close()
        simulator_idf.close()

        return r.status_code

    # TODO make /simulator generic
    @staticmethod
    def gen_fmu():
        url = "http://generator:8000/fmu/simulator"

        r = requests.get(url)
        print(r.text)
        return r.status_code

    # TODO make /simulator generic
    @staticmethod
    def get_fmu():
        url = "http://generator:8000/get_fmu/simulator"

        r = requests.get(url)
        print(r.text)
        return r.status_code
