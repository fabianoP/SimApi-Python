import subprocess
import sys
import time
import json
from pathlib import Path
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
            src_path = Path(event.src_path)
            model_name = src_path.stem
            params_path = Path('/home/deb/code/volume') / model_name / 'model_params.json'
            if not params_path.is_file():
                model_name = src_path.parent.name
                params_path = Path('/home/deb/code/volume') / model_name / 'model_params.json'

            # directory_path should be volume
            with params_path.open('r') as json_file:
                data = json.load(json_file)
                temp = data['model_params']
                params_json = temp[-1]

            print("FMU LOCATION BEFORE TASK!")
            hostname = subprocess.getoutput("cat /etc/hostname")
            result = simulator_tasks.set_model.apply_async((params_json,), queue=hostname, routing_key=hostname)
            result.get()
            print("FMU location handler COMPLETE")

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
