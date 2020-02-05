from pyfmi import load_fmu
from json_generator import JsonSerializer

"""
SimulationObject class represents an FMU model and class methods to access and run the model
"""


class SimulationObject:

    """

    """
    def __init__(self, step_size=600, final_time=72., path_to_fmu='_fmu_export_variable.fmu'):
        self.step_size = step_size
        self.final_time = 60*60*final_time
        self.model = load_fmu(path_to_fmu)
        self.model_vars = self.model.get_model_variables()

    def model_init(self):
        self.model.initialize(0, self.final_time)

    def do_time_step(self, json_input):
        fmu_input = JsonSerializer.to_dict(json_input)
        time_step = fmu_input.get('timestep')
        yshade = fmu_input.get('yshade')
        self.model.set('yShadeFMU', yshade)

        output = {'time_step': time_step}
        self.model.do_step(current_t=time_step, step_size=self.step_size, new_step=True)

        for key in self.model_vars.keys():
            output[key] = self.model.get(key)[0]

        return JsonSerializer.to_json(output)
