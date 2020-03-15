import os
import sys

from pyfmi import load_fmu

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.json_generator import JsonSerializer

"""SimulationObject class represents an FMU model and class methods to access and run the model"""


class SimulationObject:

    def __init__(self,  model_name, step_size=600, final_time=72., path_to_fmu='_fmu_export_variable.fmu'):

        """
        fmu model initialize method. Parameters originate from API.
        step_size: size of each step in seconds 600 = 10 minutes
        final_time: must be multiple of 86400 (a day in seconds) min value is 24.0,
                    converted to seconds by 60*60*final_time
        path_to_fmu: self explanatory
        """
        self.model_name = model_name
        self.step_size = step_size
        self.final_time = 60*60*final_time
        self.model = load_fmu(path_to_fmu)

        # store dict of current model variables. Key is variable name, used in do_time_step()
        self.model_vars = self.model.get_model_variables()

    def model_init(self):
        """Initialize model with start and finish time"""

        self.model.initialize(0, self.final_time)

    def do_time_step(self, json_input):
        """
        process current time_step.
        json_input: input values for current time step. Originates from API.
        json_input is converted to dict, values from dict are used to set relevant model inputs.
        calls model.do_step,
        creates new dict with output then returns output dict as json to pass back to API
        """

        fmu_input = JsonSerializer.to_dict(json_input)
        time_step = fmu_input.get('timestep')
        yshade = fmu_input.get('yshade')

        self.model.set('yShadeFMU', yshade)
        self.model.do_step(current_t=time_step, step_size=self.step_size, new_step=True)

        output = {'model_name': self.model_name, 'time_step': time_step}

        for key in self.model_vars.keys():
            output[key] = self.model.get(key)[0]

        return JsonSerializer.to_json(output)
