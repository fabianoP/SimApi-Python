import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject

""" Simple test script to. Tests functionality of the simulation_obj class"""

#  instantiate simulation obj with default values
sim_obj = SimulationObject(model_name='full_sim_test15.fmu', path_to_fmu='full_sim_test15.fmu')
sim_obj.model_init()  # initialize fmu model. Calls pyFMI model.init() and sets start and finish time
# new dictionary with inputs for fmu time step

i = 0
shade = 1.0

while i <= 259200:
    input_dict = {'time_step': i, 'yShadeFMU': shade}
    output = sim_obj.do_time_step(input_dict)
    print(output)
    i += 600

