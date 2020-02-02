from pyfmi import load_fmu
import json

model = load_fmu('_fmu_export_variable.fmu')
print(model.get_model_variables())
print(model.get_description())

opts = model.simulate_options()

print(opts)

# set number of communication points dependent on final_time and .idf steps per hour
final_time = 60*60*72.  # 72 hour simulation

model.initialize(0, final_time)
t_step = 0
step_size = 600
res = {}

fmu_outputs = open('./outputs.txt', 'w')
json_output = open('./json_output.txt', 'w')
temp = model.get_model_variables()
output = {}

print(type(output))

# write fmu output for each time step to file
while t_step < final_time:
    shading = 6
    model.set('yShadeFMU', shading)
    output['timestep'] = t_step
    res[t_step] = model.do_step(current_t=t_step, step_size=step_size, new_step=True)

    for key in temp.keys():
        output[key] = model.get(key)[0]
        fmu_outputs.write(str(key) + ' ' + str(model.get(key)) + ', ')

    fmu_outputs.write('\n')
    t_step += step_size

with json_output as json_file:
    json.dump(output, json_file)

print(output)
fmu_outputs.close()
json_output.close()
json_file.close()


