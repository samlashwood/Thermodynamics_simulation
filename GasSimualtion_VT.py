# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:52:01 2018

@author: sl4516
"""

from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo


#simulate the gas for different volumes and record the temperature
temperatures=[]
volumes=[4*np.pi*(i**2) for i in range(10,50)]
for rad in range(10,50): 
    simulation=Gas(Number=100, ContainerRadius=rad)
    for framenumber in range(100):
        simulation.next_frame(framenumber)
    print(rad)
    temperatures.append(simulation.temp())
        


def linefit(x,m,c):
    return (m*x)+c
   
#plot linear fit and VT plot     
initial_guess=[1,1] 
po,po_cov=spo.curve_fit(linefit,volumes,temperatures ,initial_guess)
fig = plt.figure()
plt.plot(volumes, temperatures)
plt.plot(volumes,[linefit(vol,po[0],po[1]) for vol in volumes],'r-',label='Fit results')
fig.suptitle('Volume-Pressure relationship for N=100')
plt.xlabel('Volume (m^2)')
plt.ylabel('Temperature (K)')
plt.show() 
print('the gradient and intercept: ', po)   