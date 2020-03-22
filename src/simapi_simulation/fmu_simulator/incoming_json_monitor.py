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
    last_input = None

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
            print("PATH INPUTS.JSON INPUT MONITOR " + str(event.src_path))
            with open(str(event.src_path), 'r') as json_file:
                data = json.load(json_file)

                print('INCOMING JSON MONITOR DATA: ' + str(data))

                input_json = data['inputs'][-1]
                print('INCOMING JSON MONITOR INPUT_JSON: ' + str(input_json))

                output_json = self.sim_obj.do_time_step(input_json)

                print('INCOMING JSON MONITOR DO_STEP OUTPUT: ' + str(output_json))

            result = simulator_tasks.post_output.apply_async((output_json,), queue='sim', routing_key='sim')
            result.get()

        elif event.src_path.endswith('model_params.json'):
            print("PATH IN MODEL PARAM INPUT MONITOR " + str(event.src_path))
            with open(str(event.src_path), 'r') as json_file:
                data = json.load(json_file)
                print('INCOMING JSON MONITOR MODEL_PARAMS DATA: ' + str(data))
                params = data['model_params'][-1]
                print('INCOMING JSON MONITOR MODEL_PARAMS PARAMS: ' + str(params))
                model_name = params['model_name']
                step_size = params['step_size']
                final_time = params['final_time']
                fmu_path = params['fmu_path']

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
