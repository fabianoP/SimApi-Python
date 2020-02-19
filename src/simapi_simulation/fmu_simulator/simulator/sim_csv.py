from pyfmi import load_fmu
import csv

# setup model #
# step_size =
# final_time = 60*60*
# model = load_fmu(path_to_fmu)
# model.get_model_variables()

with open("./csv_folder/SensorData.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    input_names = []
    for i, line in enumerate(reader):
        if i == 0:
            input_names = line

        # iterate through input names and row values
        for name, val in input_names, line:
            time_step = line.get('timestep')
            yshade = fmu_input.get('yshade')

            model.set('yShadeFMU', yshade)
            model.do_step(current_t=time_step, step_size=step_size, new_step=True)

        output = {'time_step': time_step}
        for key in self.model_vars.keys():
            output[key] = model.get(key)[0]

