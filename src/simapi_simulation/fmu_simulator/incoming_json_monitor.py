import time
import json
import psycopg2
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from simulator.simulation_obj import SimulationObject

import simulator_tasks


# TODO each time triggered request from db with model name and time step
#  instead of json upload time step and query

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
    input_set = False
    step_size = None

    def on_modified(self, event):
        connection = None
        cursor = None
        if event.src_path.endswith('model_params.json') and self.model_params_set is False:
            with open(str(event.src_path)) as json_file:
                data = json.load(json_file)

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

        # TODO romove bool condition and replace with if curr step != prev step + step size
        if event.src_path.endswith('time_step.txt') and self.input_set is False:
            self.input_set = True
            with open(str(event.src_path)) as text_file:

                text_file.seek(0)

                data = text_file.readline()

                self.current_time_step = isint(data)

                print(self.current_time_step)

            try:
                connection = psycopg2.connect(user="postgres",
                                              host="db",
                                              port="5432",
                                              database="postgres")
                cursor = connection.cursor()

                """
                select_input_query = "SELECT * " \
                                     "FROM rest_api_input;"

                cursor.execute(select_input_query)

                self.current_input = cursor.fetchall()
                for col in self.current_input:
                    print(col)
                """

                select_input_query = "SELECT input FROM rest_api_input WHERE fmu_model_id = %s AND time_step = %s;"

                cursor.execute(select_input_query, (self.model_name, self.current_time_step))

                self.current_input = cursor.fetchone()

            except (Exception, psycopg2.Error) as error:
                print("Error while getting data from PostgreSQL", error)
            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

            self.current_input = self.current_input[0]
            print(self.current_input)
            output_json = self.sim_obj.do_time_step(json.loads(self.current_input))
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
