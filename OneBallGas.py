# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 15:40:53 2018
# -*- coding: utf-8 -*-
"""
"""
Created on Thu Jan 18 12:12:58 2018

@author: sl4516
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from ClassBalls import Ball
from ClassBalls import Container

__doc__="""
A class for the simulation and animation of a particle in a container with the capability of reproducing thermodynamic properties.
Written such that it can be extended to multiple balls. 
This simulation was also obtained by moving the ball forward to its next collision.
"""

class Gas:
    timepassed=0
    def __init__(self,Number=1,ContainerRadius=10):
        """
        Initialise the Gas for a specified amount of Balls 
        """
        self.__cont=Container(ContainerRadius)
        self.__ContainerRad=ContainerRadius
        self.__ballList=[]
        for i in range(Number):
            self.__ballList.append(Ball(1,0.5,[1,3],[-20,13]))
        self.__text0 = None

    def init_figure(self):
        """
        Initialise the container diagram and add it to the plot.
        This method is called once by FuncAnimation with no arguments.
        Returns a list or tuple of the 'patches' to be animated. 
        """ 
        # add the big circle to represent the container
        BigCirc = plt.Circle((0,0), self.__ContainerRad, ec = 'b', fill = False, ls = 'solid')
        ax.add_artist(BigCirc)
        # initialise the text to be animated and add it to the plot
        self.__text0 = ax.text(-9.9,9,"f={:4d}".format(0,fontsize=12))
        patches = [self.__text0]
        # add the patch for the ball to the plot
        for b in self.__ballList:
            pch = b.get_patch()
            ax.add_patch(pch)
            patches.append(pch)
        return patches
    
    def next_frame(self, framenumber):
        """
        Do the next frame of the animation.
        This method is called by FuncAnimation with a single argument 
        representing the frame number.
        Returns a list or tuple of the 'patches' being animated.
        """
        self.__text0.set_text("f={:4d}".format(framenumber))
        patches = [self.__text0]
        for b in self.__ballList:
            if np.linalg.norm(b.pos())>=(self.__cont.rad()-b.rad()):
                b.collide(self.__cont)
            b.move(1/200)
            patches.append(b.get_patch())
        Gas.timepassed+=1./200.
        return patches
    
    def kinetic_en(self):
        energy=0
        for b in self.__ballList:
            energy+=0.5*b.mass()*(np.linalg.norm(b.vel())**2)
        return energy
    
    def pressure(self):
        totalmom=0
        for b in self.__ballList:
            totalmom+=b.MomToCont
        return totalmom/(Gas.timepassed*4*np.pi*(self.__ContainerRad**2))
    
        
        
if __name__ == "__main__":
    
    fig = plt.figure()
    ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
    ax.axes.set_aspect('equal')  

    movie = Gas()
    
    anim = animation.FuncAnimation( fig, 
                                    movie.next_frame, 
                                    init_func = movie.init_figure, 
                                    #frames = 1000, 
                                    interval = 2,
                                    blit = True)

    plt.show()
    



