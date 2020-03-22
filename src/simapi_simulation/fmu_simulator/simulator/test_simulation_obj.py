import os.path
import _pickle
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject
from simulator.json_generator import JsonSerializer

""" Simple test script to. Tests functionality of the simulation_obj class"""

#  instantiate simulation obj with default values
sim_obj = SimulationObject(model_name='work103.fmu', path_to_fmu='work103.fmu')
sim_obj.model_init()  # initialize fmu model. Calls pyFMI model.init() and sets start and finish time
# new dictionary with inputs for fmu time step
test_dict = {'timestep': 0,
             'yshade': 6.5}

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



