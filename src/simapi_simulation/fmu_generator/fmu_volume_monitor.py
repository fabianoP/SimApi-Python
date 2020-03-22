import os
import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import generator_tasks


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        path = event.src_path.rsplit('/', 1)[0]
        print('PATH IN GEN FMU MONITOR: ' + str(path))
        directory = os.listdir(str(path))
        idf = None
        epw = None
        j_son = None

        for file in directory:
            if file.endswith('.idf'):
                idf = file
            elif file.endswith('.epw'):
                epw = file
            elif file.endswith('.json'):
                j_son = file

        if idf is not None and epw is not None and j_son is not None:
            with open(str(path) + '/' + j_son, 'r') as json_file:
                data = json.load(json_file)
                json_file.close()

            result = generator_tasks.gen_fmu.apply_async((data['idf_path'],
                                                          data['epw_path'],
                                                          data['fmu_store_dir']), queue='gen', routing_key='gen')
            result.get()

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
