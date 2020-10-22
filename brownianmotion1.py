# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:39:24 2018

@author: sl4516
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpa
import numpy as np
import matplotlib.animation as animation
from ClassBalls import Ball
from ClassBalls import Container

Animate=False

__doc__="""
A class for the simulation of a hard sphere gas with the capability of reproducing thermodynamic properties. 
Set the boolean 'Animate' depending on the intended use of program.
A single Brownian particle wil be generated in the gas, with it's path traced in blue.
"""

class Gas:
    timepassed=0
    time_shift=0
    bigballpos=[0,0]
    bigballpatches=[]
    def __init__(self,Number=50,ContainerRadius=10,BallRadius=0.5,temperature=2980,ballmass=1,brownrad=2,brownmass=100):
        """
        Initialise the Gas for a specified amount of Balls in a symmetrical pattern,
        with a Gaussian speed distribution centred at 0 
        """
        self.__cont=Container(ContainerRadius)
        self.__ContainerRad=ContainerRadius
        self.__ballList=[Ball(brownmass,brownrad,[0,0],[0,0.],clr='g')]
        self.__relativetemp=(temperature/298)
        self._bmass=ballmass
        randx=[np.sqrt(self.__relativetemp)*k*np.sqrt(350) for k in np.random.normal(0,1,Number)]
        randy=[np.sqrt(self.__relativetemp)*k*np.sqrt(350) for k in np.random.normal(0,1,Number)]
        r=BallRadius+brownrad
        n=1
        Angle=0
        for i in range(Number):
            self.__ballList.append(Ball(ballmass,BallRadius,[r*np.cos(Angle),r*np.sin(Angle)],[randx[i],randy[i]]))
            circumference=np.pi*2*r
            distAngle=(np.pi*2)/(circumference/(3*BallRadius))
            Angle+=distAngle
            if (Angle+distAngle)>2*np.pi:
                r+=3*BallRadius
                n+=1
                Angle=0
        scale=self.__ContainerRad/((n*3*BallRadius)+brownrad)
        for ball in self.__ballList:
            ball.scalepos(scale) 
        self.__text0 = None
        
    def balllist(self):
        return self.__ballList
    def radius(self):
        return self.__ContainerRad
    
    def init_figure(self):
        """
        Initialise the container diagram and add it to the plot.
        This method is called once by FuncAnimation with no arguments.
        Returns a list or tuple of the 'patches' to be animated. 
        """ 
        # add the big circle to represent the container
        BigCirc = plt.Circle((0,0), self.__ContainerRad, ec = 'b', fill = False, ls = 'solid')
        ax.add_artist(BigCirc)
        # initialise the axis to be animated and add it to the plot
        self.__text0 = ax.text(-9.9,9,"f={:4d}".format(0,fontsize=12))
        patches = [self.__text0]
        # add the patches for the balls to the plot
        for b in self.__ballList:
            pch = b.get_patch()
            ax.add_patch(pch)
            patches.append(pch)
        return patches
    
    def next_frame(self, framenumber):
        """
        Do the next frame of the animation.
        This calculates the time to the next collison of any
        gas particles and moves the animation on to the next collision. 
        If the 2 balls are next to each other and moving towards each other, they collide.
        This method is called by FuncAnimation with a single argument 
        representing the frame number.
        Returns a list or tuple of the 'patches' being animated.
        """
        
        if Animate==True:
            self.__text0.set_text("f={:4d}".format(framenumber))
            patches = [self.__text0]
        if Animate==False:
            patches=[]
        timeallball=[]
        for ball in self.__ballList:
            time1ball=[]
            balls=self.__ballList.copy()
            balls.append(self.__cont)
            balls.remove(ball)
            for otherball in balls:
                othertime=ball.time_to_collision(otherball)
                if isinstance(othertime,int)==True or isinstance(othertime,float)==True:
                    time1ball.append(othertime)
                    if othertime==0:
                        ball.collide(otherball)
                        break
            timeallball.append(min(time1ball))
            if min(time1ball)==0:
                break
        
        for b in self.__ballList:
            b.move(min(timeallball))
            patches.append(b.get_patch())
        Gas.timepassed+=min(timeallball)
        
         #Animate the Big ball and its path using arrow patches
        large=self.balllist()[0]
        largepos=large.pos()
        if np.linalg.norm(largepos)!=0:
            patchl= mpa.Arrow(Gas.bigballpos[0],Gas.bigballpos[1],(largepos[0]-Gas.bigballpos[0]),(largepos[1]-Gas.bigballpos[1]),width=0.1,color='c')    
            Gas.bigballpatches.append(patchl)
            Gas.bigballpos=largepos
        if Animate==True:
            if len(Gas.bigballpatches)!=0:
                for p in Gas.bigballpatches:
                    ax.add_patch(p)
                    patches.append(p)
        
        #check to see if KE/momentum conserved, and see pressure change
        """
        if Gas.timepassed>5 and Gas.timepassed<10 :
            print(self.kinetic_en(), self.momentum())
            print(self.pressure())
        """    
        return patches
    
    #returns the total kinetic energy of the gas
    def kinetic_en(self):
        energy=0
        for b in self.__ballList:
            energy+=0.5*b.mass()*(np.linalg.norm(b.vel())**2)
        return energy
    
    #returns the pressure due to the gas at a given time  
    def pressure(self):
        totalmom=0
        for b in self.__ballList:
            totalmom+=b.MomToCont
        return totalmom/(Gas.timepassed*4*np.pi*(self.__ContainerRad**2))
    
    #returns the total particle momentum of the gas
    def momentum(self):
        momen=0
        for b in self.__ballList:
            momen+=np.linalg.norm(b.mass()*b.vel())
        return momen
    
    #returns the mean and varience of velocity distribution
    def velocitystats(self):
        meanv=np.mean([np.linalg.norm(bal.vel()) for bal in self.balllist()])
        varv=np.var([np.linalg.norm(bal.vel()) for bal in self.balllist()])
        return [meanv,varv]
    
    #returns the temperature of the gas
    def temp(self):
        temps=((1.38e-23)**-1)*self._bmass*self.velocitystats()[0]**2  
        return temps
        
if Animate==True:    
#code to initialise the animation, if required        
    if __name__ == "__main__":
        movie = Gas()
        fig = plt.figure()
        ax = plt.axes(xlim=(-1*movie.radius(), movie.radius()), ylim=(-1*movie.radius(), movie.radius()))
        ax.axes.set_aspect('equal')  
    
        
    
        anim = animation.FuncAnimation( fig, 
                                        movie.next_frame, 
                                        init_func = movie.init_figure, 
                                        #frames = 1,
                                        interval = 2,
                                        blit = True)
        
        plt.show()

#code to produce the path of the brownian particle over a long time without animation (takes >3hours)

if Animate==False:
    gas=Gas()
    def ray(a):
        return (2*a/50)*np.exp(-1*(a**2)/50)
    positions=[]
    for k in range(100000):
        gas.next_frame(k)
        positions.append(np.linalg.norm(gas.bigballpos))
    fig = plt.figure()
    ax = plt.axes(xlim=(-1*gas.radius(), gas.radius()), ylim=(-1*gas.radius(), gas.radius()))
    ax.axes.set_aspect('equal')         
    for m in gas.init_figure()[1:]:
        ax.add_patch(m)
    for i in gas.bigballpatches:
        ax.add_patch(i) 
    plt.show()
    plt.savefig('Brownian_path2')
    fig = plt.figure()
    plt.hist(positions, bins=50, normed=1)
    plt.plot(np.linspace(0,10,1000), [ray(p) for p in np.linspace(-10,10,1000)])