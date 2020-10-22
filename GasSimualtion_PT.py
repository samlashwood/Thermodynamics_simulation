# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:29:35 2018

@author: sl4516
"""

from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

#simulate the gas for different temperatures and record the pressure
pressures=[]
temperatures=[298*i for i in range(1,15)]
for temperature1 in temperatures: 
    simulation=Gas(Number=100,speed=1, ContainerRadius=1, temperature=temperature1)
    for framenumber in range(100):
        simulation.next_frame(framenumber)     
    pressures.append(simulation.pressure())
        


def linefit(x,m,c):
    return (m*x)+c

#plot linear fit and PT plot  
initial_guess=[1,1] 
po,po_cov=spo.curve_fit(linefit,temperatures,pressures,initial_guess)
fig = plt.figure()
plt.plot(temperatures, pressures)
plt.plot(temperatures,[linefit(temp,po[0],po[1])  for temp in temperatures],'r-',label='Fit results')
fig.suptitle('Temperature-Pressure relationship for N=1000, R=10')
plt.xlabel('Temperature (K)')
plt.ylabel('Pressure (Pa)')
plt.show()  
print('the gradient and intercept: ', po)    