# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:15:51 2018

@author: sl4516
"""

from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

#simulate the gas for different number of particles and record the pressure
pressures=[]
numbers=range(50,700,50)
for num in range(50,700,50): 
    simulation=Gas(Number=num, ContainerRadius=50)
    for framenumber in range(100):
        simulation.next_frame(framenumber)
    print(num)
    pressures.append(simulation.pressure())
        


def linefit(x,m,c):
    return (m*x)+c

#plot linear fit and NP plot     
initial_guess=[1,1] 
po,po_cov=spo.curve_fit(linefit,numbers,pressures,initial_guess)
fig = plt.figure()
plt.plot(numbers, pressures)
plt.plot(numbers,[linefit(vol,po[0],po[1]) for vol in numbers],'r-',label='Fit results')
fig.suptitle('Number-Pressure relationship for R=50')
plt.xlabel('Nuumber of particles')
plt.ylabel('Pressure (Pa)')
plt.show()
print('the gradient and intercept: ', po)   