# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:05:50 2018

@author: sl4516
"""

from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

#simulate the gas for different volumes and record the pressure
pressures=[]
volumes=[4*np.pi*(i**2) for i in range(10,50)]
for rad in range(10,50): 
    simulation=Gas(Number=100, ContainerRadius=rad, temperature=298)
    for framenumber in range(100):
        simulation.next_frame(framenumber)   
    print(rad)
    pressures.append(simulation.pressure())
        

#plot linear fit and 1/p plot, as expected from ideal gas law
def linefit(x,m,c):
    return (m*x)+c
    
initial_guess=[1e25,-1] 
po,po_cov=spo.curve_fit(linefit,volumes,[1/p for p in pressures] ,initial_guess)
fig = plt.figure()
plt.plot(volumes, [1/p for p in pressures])
plt.plot(volumes,[linefit(vol,po[0],po[1])  for vol in volumes],'r-',label='Fit results')
fig.suptitle('Volume-Pressure relationship for N=100, R=10')
plt.xlabel('Volume (m^2)')
plt.ylabel('1/Pressure (1/Pa)')
plt.show()  
print('the gradient and intercept: ', po) 