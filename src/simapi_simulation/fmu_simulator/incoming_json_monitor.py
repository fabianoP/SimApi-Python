import sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from simulator.simulation_obj import SimulationObject

import simulator_tasks


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    sim_obj = None
    header = None
    current_input = None
    previous_inputs = []

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # TODO inputs triggered twice. NEED FIX!
        if event.src_path.endswith('inputs.json'):
            with open(str(event.src_path), 'r') as json_file:
                data = json.load(json_file)

                print('data: ' + str(data))

                self.current_input = data['inputs'][-1]

            if self.current_input not in self.previous_inputs:
                self.previous_inputs.append(self.current_input)

                print(self.previous_inputs)

                output_json = self.sim_obj.do_time_step(self.current_input)

                print(output_json)

                simulator_tasks.post_output.apply_async((output_json, self.header),
                                                        queue='sim',
                                                        routing_key='sim')
            else:
                print("Input already seen!")

        elif event.src_path.endswith('model_params.json'):
            with open(str(event.src_path), 'r') as json_file:
                data = json.load(json_file)

                params = data['model_params'][-1]
                model_name = params['model_name']
                step_size = params['step_size']
                final_time = params['final_time']
                fmu_path = params['fmu_path']
                print(f'model_params type {type(step_size)}')
                print(f'model_params type {type(final_time)}')
                self.header = {'Authorization': params['Authorization']}

                self.sim_obj = SimulationObject(model_name=model_name, step_size=int(step_size),
                                                final_time=float(final_time),
                                                path_to_fmu=fmu_path)
                self.sim_obj.model_init()

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
