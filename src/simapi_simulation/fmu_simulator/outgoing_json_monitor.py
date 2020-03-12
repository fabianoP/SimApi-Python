import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import simulator_tasks


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

        if event.src_path.endswith('outputs.json'):
            with open(event.src_path, 'r') as json_file:
                data = json.load(json_file)

                temp = data['outputs']

                input_json = temp.slice(-1)

            result = simulator_tasks.model_input.apply_async((input_json,))
            result.forget()

    def on_modified(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
