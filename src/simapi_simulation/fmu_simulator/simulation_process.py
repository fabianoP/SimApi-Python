import os
import subprocess
import time
import json
from pathlib import Path

import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from simulator.simulation_obj import SimulationObject

import simulator_tasks


def isint(value):
    try:
        time_step = int(value)
        return time_step
    except ValueError:
        return False


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.json", "*.txt"]

    sim_obj = None
    model_name = None
    header = None
    current_time_step = None
    current_input = None
    model_params_set = False
    first_input_set = False
    step_size = None
    prev_time_step = 0

    def on_modified(self, event):
        #  Model initialized here when model_params.json is updated
        if event.src_path.endswith('model_params.json') and self.model_params_set is False:

            with open(str(event.src_path)) as json_file:

                data = json.load(json_file)  # TODO Broken

                if len(data) > 0:
                    params = data['model_params'][-1]
                    self.model_name = params['model_name']
                    self.step_size = params['step_size']
                    final_time = params['final_time']
                    fmu_path = params['fmu_path']

                    self.header = {'Authorization': params['Authorization']}

                    self.sim_obj = SimulationObject(model_name=self.model_name, step_size=int(self.step_size),
                                                    final_time=float(final_time),
                                                    path_to_fmu=fmu_path)
                    self.sim_obj.model_init()
                    self.model_params_set = True
                    os.system('rm /home/deb/code/store_incoming_json/model_params.json')

        # simulation time steps run here when time_step.txt is updated
        if event.src_path.endswith('time_step.txt') and self.model_params_set is True:
            with open(str(event.src_path)) as text_file:

                text_file.seek(0)

                data = text_file.readline()

                self.current_time_step = isint(data)
                print("Current time Step read from file: " + str(self.current_time_step))

            if self.current_time_step == self.prev_time_step + int(self.step_size) or not self.first_input_set:
                self.first_input_set = True
                self.prev_time_step = self.current_time_step

                graphql_url = 'http://web:8000/graphql/'

                input_query = """
                {{
                    inputs(modelN: "{0}", tStep: {1}) {{
                        inputJson
                    }}
                }}
                """.format(str(self.model_name), self.current_time_step)
                r = requests.get(url=graphql_url, json={'query': input_query})
                print("INPUT_QUERY: " + input_query)
                print("STATUS: input_query " + str(r.status_code))
                print("TEXT: input_query " + r.text)

                graphql_response = r.json()['data']['inputs'][0]['inputJson']

                self.current_input = json.loads(json.loads(graphql_response))

                print("\ninput: " + str(self.current_input))

                # run do_step for current time step with current inputs
                output_json = self.sim_obj.do_time_step(self.current_input)

                print('OUTPUT FOR MODEL: ' + self.model_name + ' | ' + output_json)
                # task uploads output to db
                hostname = subprocess.getoutput("cat /etc/hostname")
                result = simulator_tasks.post_output.apply_async((output_json, self.header),
                                                                 queue=hostname,
                                                                 routing_key=hostname)
                result.get()

                # when last time step has completed free and terminate instance
                if self.current_time_step == self.sim_obj.final_time - int(self.step_size):
                    self.sim_obj.model.free_instance()

                    swarm_check = Path('/home/deb/code/isSwarm.txt')
                    if swarm_check.exists():
                        os.system('rm /home/deb/code/isSwarm.txt')


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
