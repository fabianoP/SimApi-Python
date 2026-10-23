import json
import sys
import time
from pathlib import Path

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import generator_tasks


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    def process(self, event):
        directory = Path(event.src_path).parent
        print(f"PATH IN GEN FMU MONITOR: {directory}")
        files = list(directory.iterdir())

        if not all(any(path.suffix == suffix for path in files) for suffix in (".idf", ".epw", ".json")):
            return

        with Path(event.src_path).open(encoding="utf-8") as json_file:
            data = json.load(json_file)

        generator_tasks.gen_fmu.apply_async(
            (data["idf_path"], data["epw_path"], data["fmu_store_dir"]),
            queue="gen",
            routing_key="gen",
        )

    def on_created(self, event):
        if not event.is_directory:
            self.process(event)


if __name__ == "__main__":
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
