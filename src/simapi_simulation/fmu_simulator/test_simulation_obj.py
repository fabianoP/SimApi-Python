from .simulation_obj import SimulationObject
from .json_generator import JsonSerializer

""" Simple test script to. Tests functionality of the simulation_obj class"""

sim_obj = SimulationObject()  # instantiate simulation obj with default values
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

print(json_output)

test_dict = {'timestep': 1800,
             'yshade': 1}

json_input = JsonSerializer.to_json(test_dict)
json_output = sim_obj.do_time_step(json_input)

print(json_output)
