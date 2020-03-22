import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import simulator_tasks

# TODO will trigger a background script and pass the path of fmu as arg.
#  Background script will monitor inputs and set model params, do_step ... etc.
#  post output to API


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

        # TODO Write model_params to input folder
        print("EVENT IN FMU LOC MONITOR: " + str(event.src_path))
        if event.src_path.endswith('.zip'):

            fmu_name = event.src_path.rsplit('/', 1)[1]
            model_name = str(fmu_name).rsplit('.', 1)[0]
            print("MODEL NAME IN FMU LOC MONITOR: " + str(model_name))
            # directory_path should be volume
            with open('/home/deb/code/volume/' + model_name + '/model_params.json', 'r') as json_file:
                print(f'SEARCH FOR LIST INDICES ERROR!')
                data = json.load(json_file)
                print(f'FMU LOC JSON.LOAD DATA = {data}')
                temp = data['model_params']
                print(f'FMU LOC DATA[model_params] = {temp}')
                params_json = temp[-1]
                print(f'FMU LOC params_json = {params_json}')

            result = simulator_tasks.set_model.apply_async((params_json,), queue='sim', routing_key='sim')
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
