# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:07:24 2018

@author: samla
"""


from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

#simulate the gas and record the pressure at different times
pressures=[]
times=[]
simulation=Gas(Number=100,ContainerRadius=10,BallRadius=0.5,temperature=298,ballmass=1.67e-27,speed=5)
for framenumber in range(1000):
    simulation.next_frame(framenumber)
    times.append(simulation.timepassed)
    pressures.append(simulation.pressure())
        
#plot pressure-time plot     
fig = plt.figure()
plt.plot(times, pressures)
fig.suptitle('Time-Pressure relationship for 100 balls at R=10')
plt.xlabel('Time passed (s)')
plt.ylabel('Pressure (Pa)')
plt.show()   