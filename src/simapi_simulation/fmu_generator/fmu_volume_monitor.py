import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import generator_tasks
from simulator_api.generator_client import GeneratorClient


class MyHandler(PatternMatchingEventHandler):
    # patterns = ["*.idf", "*.epw"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        directory = os.listdir(event.src_path)
        idf = None
        epw = None

        for file in directory:
            if file.endswith('.idf'):
                idf = file
            elif file.endswith('.epw'):
                epw = file

        if idf is not None and epw is not None:
            fmu_store_dir = '/home/fmu/code/fmu_location/'  # TODO
            result = generator_tasks.gen_fmu.apply_async((idf, epw, fmu_store_dir))
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
