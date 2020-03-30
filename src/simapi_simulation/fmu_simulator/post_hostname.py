import subprocess

import requests
import polling2


hostname_url = 'http://web:8000/hostname/'

hostname = subprocess.check_output("cat /etc/hostname", shell=True)

hostname_data = {
    'hostname': hostname
}

polling2.poll(
        lambda: requests.post(hostname_url, data=hostname_data) == 200,
        step=1,
        poll_forever=True)
