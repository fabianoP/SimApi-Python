import os as O

import pylab as P
import numpy as N

from pyfmi import load_fmu
import matplotlib.pyplot as plt
from timeit import default_timer as timer

model = load_fmu('./eplus/_fmu_export_actuator.fmu')

opts = model.simulate_options()

# set number of communication points dependent on final_time and .idf steps per hour
final_time = 60*60*72.  # 72 hour simulation
idf_steps_per_hour = 6
ncp = final_time/(3600./idf_steps_per_hour)
opts['ncp'] = ncp

# start = timer()
model.initialize(0, final_time)
# end = timer()
#
# f.write(str(end - start))
# f.close()

t_step = 0
res = {}

outputs = open("outputs.txt", "x")
while t_step < final_time:
    res[t_step] = model.do_step(current_t=t_step, step_size=600, new_step=True)
    outputs.write('TRoo ' + str(model.get('TRoo')) + ' ISolExt ' + str(model.get('ISolExt')))
    outputs.write('\n')
    t_step += 600

outputs.close()

file = open("res.txt", "x")

for step in res:
    file.write(str(step))
    file.write('\n')

file.close()

"""
# run simulation and return results
res = model.simulate(start_time=0., final_time=final_time, options=opts)
print(res.keys())  # show result variables names

# plot results
fig, ax1 = plt.subplots()
ax1.plot(res['time'], res['TRoo'], 'b-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Room Temperature', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(res['time'], res['ISolExt'], 'r.')
ax2.set_ylabel('Solar Radiation', color='r')
ax2.tick_params('y', colors='r')
fig.tight_layout()
plt.show()
"""