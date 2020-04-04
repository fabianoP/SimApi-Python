import subprocess
import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import simulator_tasks


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.zip"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        if event.src_path.endswith('.zip'):
            print("FMU LOCATION!")
            fmu_name = event.src_path.rsplit('/', 1)[1]
            model_name = str(fmu_name).rsplit('.', 1)[0]

            # directory_path should be volume
            with open('/home/deb/code/volume/' + model_name + '/model_params.json', 'r') as json_file:
                data = json.load(json_file)
                temp = data['model_params']
                params_json = temp[-1]

            print("FMU LOCATION BEFORE TASK!")
            hostname = subprocess.getoutput("cat /etc/hostname")
            result = simulator_tasks.set_model.apply_async((params_json,), queue=hostname, routing_key=hostname)
            result.get()
            print("FMU location handler COMPLETE")

            subprocess.getoutput('chmod -R  a+rw /home/deb/code/fmu_location/ *')

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
