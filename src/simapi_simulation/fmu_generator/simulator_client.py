import requests


class SimulatorClient:

    @staticmethod
    def put_fmu(container='0.0.0.0'):
        url = "http://" + container + ":8000/test"
        print('IN POST FMU')
        fmu_name = container + '.fmu'
        # fmu = open("/home/fmu/code/energy/test/" + fmu_name, 'rb')
        print('IN POST FMU AFTER OPEN')
        # file = {'fmu': (fmu_name, open("/home/fmu/code/energy/test/" + fmu_name, 'rb'))}

        with open("/home/fmu/code/energy/test/" + fmu_name, 'rb') as f:
            r = requests.put(url,
                             data=f,
                             headers={'X-File-Name': fmu_name,
                                      'Content-Disposition': 'form-data; name="{0}"; filename="{0}"'.format(
                                          fmu_name),
                                      'content-type': 'multipart/form-data'})

        # r = requests.post(url, files=file)
        print('IN POST FMU AFTER POST')
        # fmu.close()
        return r.status_code
