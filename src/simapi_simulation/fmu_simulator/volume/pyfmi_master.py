import os as O

import pylab as P
import numpy as N

from pyfmi import load_fmu

model = load_fmu('_fmu_export_actuator.fmu')

opts = model.simulate_options()

# set number of communication points dependent on final_time and .idf steps per hour
final_time = 60*60*72.  # 72 hour simulation
idf_steps_per_hour = 6 # 10 mins per step
ncp = final_time/(3600./idf_steps_per_hour)  # number of communication points (ncp) not currently used
opts['ncp'] = ncp

model.initialize(0, final_time)
t_step = 0
res = {}

outputs = open("outputs.txt", "x")

# write fmu output for each time step to file
while t_step < final_time:
    res[t_step] = model.do_step(current_t=t_step, step_size=600, new_step=True)
    outputs.write('TRoo ' + str(model.get('TRoo')) + ' ISolExt ' + str(model.get('ISolExt')))
    outputs.write('\n')
    t_step += 600

outputs.close()

file = open("res.txt", "x")

# write time step values to file
for step in res:
    file.write(str(step))
    file.write('\n')

file.close()
