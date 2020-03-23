import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject

""" Simple test script to. Tests functionality of the simulation_obj class"""

#  instantiate simulation obj with default values
sim_obj = SimulationObject(model_name='nearly85.fmu', path_to_fmu='nearly85.fmu')
sim_obj.model_init()  # initialize fmu model. Calls pyFMI model.init() and sets start and finish time
# new dictionary with inputs for fmu time step


test_dict = {'time_step': 0,
             'yShadeFMU': 1}


# simulation object do_time_step method returns json
json_output = sim_obj.do_time_step(test_dict)

print(json_output)

test_dict = {'time_step': 600,
             'yShadeFMU': 2}

json_output = sim_obj.do_time_step(test_dict)

print(json_output)

test_dict = {'time_step': 1200,
             'yShadeFMU': 3}

json_output = sim_obj.do_time_step(test_dict)

print(json_output)

test_dict = {'time_step': 1800,
             'yShadeFMU': 1}

json_output = sim_obj.do_time_step(test_dict)

print(json_output)


test_dict = {'time_step': 2400,
             'yShadeFMU': 3}

json_output = sim_obj.do_time_step(test_dict)

print(json_output)
