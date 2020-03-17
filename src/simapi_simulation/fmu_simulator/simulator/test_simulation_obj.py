import os.path
import _pickle
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject
from simulator.json_generator import JsonSerializer

""" Simple test script to. Tests functionality of the simulation_obj class"""

#  instantiate simulation obj with default values
sim_obj = SimulationObject(model_name='work94.fmu', path_to_fmu='work94.fmu')
sim_obj.model_init()  # initialize fmu model. Calls pyFMI model.init() and sets start and finish time
# new dictionary with inputs for fmu time step
test_dict = {'timestep': 0,
             'yshade': 1}

# simulation object do_time_step method takes json as parameter so convert dict to json
json_input = JsonSerializer.to_json(test_dict)

# simulation object do_time_step method returns json
json_output = sim_obj.do_time_step(json_input)

print(json_output)

test_dict = {'timestep': 600,
             'yshade': 2}

json_input = JsonSerializer.to_json(test_dict)
json_output = sim_obj.do_time_step(json_input)

print(json_output)

test_dict = {'timestep': 1200,
             'yshade': 3}

json_input = JsonSerializer.to_json(test_dict)
json_output = sim_obj.do_time_step(json_input)

print("OUTPUT BEFORE PICKLE")
print(json_output)


with open('company_data.pkl', 'wb') as output:
    _pickle.dump(sim_obj, output, -1)


with open('company_data.pkl', 'rb') as input_pick:
    sim_obj_pickle = _pickle.load(input_pick)


test_dict = {'timestep': 1800,
             'yshade': 1}

json_input = JsonSerializer.to_json(test_dict)
json_output = sim_obj_pickle.do_time_step(json_input)

print("OUTPUT PICKLE")
print(json_output)


test_dict = {'timestep': 2400,
             'yshade': 3}

json_input = JsonSerializer.to_json(test_dict)
json_output = sim_obj_pickle.do_time_step(json_input)

print("OUTPUT PICKLE")
print(json_output)


