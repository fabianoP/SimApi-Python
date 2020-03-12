import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

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
            model_name = event.src_path.rsplit('/', 1)[1]  # TODO test if model name returned from split
            GeneratorClient.post_files(model_name)

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
