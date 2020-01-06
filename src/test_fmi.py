import os as O

import pylab as P
import numpy as N

from pyfmi import load_fmu

model = load_fmu('/home/slickrick/Django/sim-api/eplus/bouncingBall.fmu')

res = model.simulate()
h_res = res['h']
v_res = res['v']
t = res['time']

# assert N.abs(res.final('h') - (0.0424044)) < 1e-4
with_plots = True
# Plot the solution
if with_plots:
    # Plot the height
    fig = P.figure()
    P.clf()
    P.subplot(2, 1, 1)
    P.plot(t, h_res)
    P.ylabel('Height (m)')
    P.xlabel('Time (s)')
    # Plot the velocity
    P.subplot(2, 1, 2)
    P.plot(t, v_res)
    P.ylabel('Velocity (m/s)')
    P.xlabel('Time (s)')
    P.suptitle('FMI Bouncing Ball')
    P.show()
print(res)
