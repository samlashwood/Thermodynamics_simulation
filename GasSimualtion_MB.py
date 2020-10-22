# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:33:55 2018

@author: sl4516
"""
from ClassGas import Gas
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo

"""
Code to plot a histogram of the paricle velocities and plot the theoretical Maxwell Boltzmann distribution on the same axes.
Also calculates the theoretical Vrms and obtains a mean Vrms for the velocity data from multiple simulations.
"""
NO=800
nobins=30

#simulate the gas 
simulation=Gas(Number=NO, ContainerRadius=4e-11, temperature=298)
for framenumber in range(2):
    simulation.next_frame(framenumber)    

#plot a probability density histogram of the velocities        
velocities=[np.linalg.norm(ball.vel()) for ball in simulation.balllist()]
fig = plt.figure()
plt.hist(velocities, bins=nobins, normed=1)

#Add errors from a counting experiment to the data
bins, bin_edges = np.histogram(velocities, bins=nobins, density=True)
bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

plt.errorbar(
    bin_centers,
    bins,
    yerr = (bins**0.5)/800,
    marker = '+',
    ls='none')

#plot the 2D Maxwell-Boltzmann distribution- All parameters are fixed  
def maxbolt2D(v):
    a=(1.67e-27/(298*1.38e-23))
    return a*v*np.exp(-0.5*a*(v**2))

mbp=[maxbolt2D(v) for v in np.linspace(0,8000,10000)]
plt.plot(np.linspace(0,8000,10000),mbp,'k-',label='Fit results')

fig.suptitle('Hydrogen Velocity distribution for N=800, T=298K')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Probability density')
plt.show()
    
#obtain a mean vrms for velocities
vrms=[(np.var(velocities)+np.mean(velocities)**2)**0.5]
for a in range(100):
    for framenumber in range(2):
        simulation.next_frame(framenumber)    
    velocities=[np.linalg.norm(ball.vel()) for ball in simulation.balllist()]
    vrms.append((np.var(velocities)+np.mean(velocities)**2)**0.5)

    
print('The mean vrms of the velocities is', np.mean(vrms)) 
print('The vrms from the 2D M-B distribution is', (((1.67e-27)**-1)*2*1.38e-23*298)**0.5) 



