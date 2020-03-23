import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from simulator_api.generator_client import GeneratorClient


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

        if event.src_path.endswith('.json'):
            print("PATH IN VOLUME MONITOR " + event.src_path)
            directory_path = event.src_path.rsplit('/', 1)[0]  # TODO this works
            directory = os.listdir(str(directory_path))
            idf = None
            epw = None
            json_file = None

            for file in directory:
                if file.endswith('.idf'):
                    print("IDF FOUND IN VOL MON")
                    print(file)
                    idf = file
                elif file.endswith('.epw'):
                    print("EPW FOUND IN VOL MON")
                    print(file)
                    epw = file
                elif file.endswith('.json'):
                    print("JSON FOUND IN VOL MON")
                    print(file)
                    json_file = file

            if idf is not None and epw is not None and json_file is not None:
                model_name = str(directory_path).rsplit('/', 1)[1]

                print("VOLUME MONITOR: GEN CLIENT MODEL NAME: " + model_name)
                GeneratorClient.post_files(model_name)

        # TODO else pass failure message

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
