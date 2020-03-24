import sys
import time
import json
from json import JSONDecodeError

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from simulator.simulation_obj import SimulationObject

import simulator_tasks

# TODO each time triggered request from db with model name and time step
#  instead of json upload time step and query


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]

    sim_obj = None
    header = None
    current_input = None
    previous_inputs = []
    model_params_set = False
    input_set = False

    def on_modified(self, event):
        if event.src_path.endswith('model_params.json') and self.model_params_set is False:
            with open(str(event.src_path)) as json_file:
                data = json.load(json_file)

                params = data['model_params'][-1]
                model_name = params['model_name']
                step_size = params['step_size']
                final_time = params['final_time']
                fmu_path = params['fmu_path']

                self.header = {'Authorization': params['Authorization']}

                self.sim_obj = SimulationObject(model_name=model_name, step_size=int(step_size),
                                                final_time=float(final_time),
                                                path_to_fmu=fmu_path)
                self.sim_obj.model_init()
                self.model_params_set = True

        if event.src_path.endswith('inputs.json') and self.input_set is False:
            self.input_set = True
            with open(str(event.src_path)) as json_file:

                data = json.load(json_file)

                self.current_input = data['inputs'][-1]
                print(self.current_input)

            output_json = self.sim_obj.do_time_step(self.current_input)
            print(output_json)
            result = simulator_tasks.post_output.apply_async((output_json, self.header),
                                                             queue='sim',
                                                             routing_key='sim')
            result.get()

        elif self.input_set is True:
            self.input_set = False


if __name__ == '__main__':
    path = '/home/deb/code/store_incoming_json'
    observer = Observer()
    observer.schedule(MyHandler(), path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
