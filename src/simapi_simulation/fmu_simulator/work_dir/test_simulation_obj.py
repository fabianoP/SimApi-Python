from simulation_obj import SimulationObject
from json_generator import JsonSerializer


sim_obj = SimulationObject()
sim_obj.model_init()

test_dict = {'timestep': 0,
             'yshade': 1}

json_input = JsonSerializer.to_json(test_dict)
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
