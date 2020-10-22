# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 23:44:59 2018

@author: samla
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt


__doc__="""A Ball class to model gas molecules"""
class Ball:
    MomToCont=0
    def __init__(self, mass, radius, position, velocity, clr='r'):
        self.__mass=mass
        self.__rad=radius
        if type(position)!=list:
            raise Exception("position must be a vector (list)")
        self.__pos=np.array(position)
        if type(velocity)!=list:
            raise Exception("velocity must be a vector (list)")
        self.__vel=np.array(velocity)
        self.__patch=plt.Circle(self.__pos, self.__rad, fc=clr)
    def mass(self):
        return self.__mass
    def rad(self):
        return self.__rad
    def pos(self):
        return self.__pos    
    def vel(self):
        return self.__vel
    def setvel(self, array):
        self.__vel=array
    
    #method to move ball's position forward a specified amount of time
    def move(self,dt):
        self.__pos=self.__pos+(self.__vel*dt)
        self.__patch.center = self.__pos
        return self
    
    #method to project movement of ball without moving it, to check if balls will collide
    def theorMove(self,dt):
        a=self.__pos+(self.__vel*dt)        
        return a
    
    #method to scale position, for gas initialisation
    def scalepos(self,a):
        self.__pos=a*self.__pos
        
    #return the patch of the ball for the animation
    def get_patch(self):
        return self.__patch
    
    """
    Method to calculate the time until the next collision with the container or another ball.
    Balls must be moving toward each other to collide, very small times are counted as 0
    """
    def time_to_collision(self, other):
        rel_vel_sq=np.dot(self.__vel-other.__vel,self.__vel-other.__vel)
        rel_pos_sq=np.dot(self.__pos-other.__pos,self.__pos-other.__pos)
        pos_dot_vel=np.dot(self.__pos-other.__pos,self.__vel-other.__vel)
        if type(other)==Ball:
            d_time=np.roots(np.array([rel_vel_sq,2*pos_dot_vel,(rel_pos_sq-(self.__rad+other.__rad)**2)]))
            nextcol=[]
            for i in range(len(d_time)):
                if d_time[i]>=-1e-6 and isinstance(d_time[i],float)==True or isinstance(d_time[i],int)==True:
                    if np.linalg.norm(self.theorMove(0.001)-other.theorMove(0.001))<np.linalg.norm(self.pos()-other.pos()): 
                        if np.abs(d_time[i])<1e-6:
                            d_time[i]=0
                        nextcol.append(d_time[i])
                else:
                    pass
            if nextcol:
                return min(nextcol)
        elif type(other)==Container:
            d_time=np.roots(np.array([rel_vel_sq,2*pos_dot_vel,rel_pos_sq-(self.__rad-other.__rad)**2]))
            for i in range(len(d_time)):
                if d_time[i]>=-0.001 and isinstance(d_time[i],float)==True or isinstance(d_time[i],int)==True:
                    if np.abs(d_time[i])<0.001:
                        d_time[i]=0
                    return d_time[i]
                else:
                    pass
        else:
            raise Exception("Must collide with another Ball or the Container")
    """        
    Method for collision of balls/container that can be generalized to 3D- 
    Works out final velocities in elastic collision
    """
    def collide(self, other):
        if isinstance(other,Container)==False:
            parallell_vel_self=np.dot(self.__pos-other.__pos, self.__vel)*(self.__pos-other.__pos)*(np.linalg.norm(self.__pos-other.__pos))**-2
            perpen_vel_self=self.__vel-parallell_vel_self
            parallell_vel_other= np.dot(self.__pos-other.__pos, other.__vel)*(self.__pos-other.__pos)*(np.linalg.norm(self.__pos-other.__pos))**-2
            perpen_vel_other=other.__vel-parallell_vel_other
            parallell_vel_other_fin=(2*self.__mass*parallell_vel_self+((other.__mass-self.__mass)*parallell_vel_other))/(self.__mass+other.__mass)
            parallell_vel_self_fin=(2*other.__mass*parallell_vel_other+((self.__mass-other.__mass)*parallell_vel_self))/(self.__mass+other.__mass)           
            self.__vel=perpen_vel_self+parallell_vel_self_fin
            other.__vel=perpen_vel_other+parallell_vel_other_fin
        elif isinstance(other,Container)==True:
            parallell_vel_selfc=np.dot(self.__pos*(np.linalg.norm(self.__pos)**-1),self.__vel)*(self.__pos)*(np.linalg.norm(self.__pos))**-1
            perpen_vel_selfc=self.__vel-parallell_vel_selfc
            self.__vel=perpen_vel_selfc-parallell_vel_selfc
            Ball.MomToCont+=2*np.linalg.norm(parallell_vel_selfc)*self.__mass
            
            
            
__doc__="""Container class that inherits from Ball, centred at the origin with a specifiable radius"""           
class Container(Ball):
    def __init__(self,cont_rad):
        Ball.__init__(self,0,cont_rad,[0,0],[0,0])
        
        
