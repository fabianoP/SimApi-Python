import subprocess
import time

import requests
import polling2


hostname_url = 'http://web:8000/hostname/'

hostname = subprocess.getoutput("cat /etc/hostname")

hostname_data = {
    'hostname': hostname
}

time.sleep(30)

polling2.poll(
        lambda: requests.post(hostname_url, data=hostname_data).status_code == 201,
        step=30,
        poll_forever=True)


