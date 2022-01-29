# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 17:18:52 2022

@author: Ryan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 15:26:33 2022

@author: Ryan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass
import math
y_max=0
total_range=0

#angles=list(range(-80,80,10))
angles=[10,20,30,40,50]
height=10
V=40
D=.004
G=9.80665
delt_t=.001

theta=20




x=0   
y=height
mass=(4/3)*(3.141592653)*((D/2)**3)*(1000)
rho=1.225
A=(3.141592653*(D/2)**2)
Cd=rho*.45*A/2
print(mass)
df_theta=pd.DataFrame([])
def Trejectory(theta,V,x,y,df_theta):
    theta_name=str(theta)
    theta=(theta*3.141592653/180)
    vx=V*math.cos(theta)
    vy=V*math.sin(theta)
    
    total_range=(V*math.cos(theta)/G)*(V*math.sin(theta)+(V**2*math.sin(theta)**2+2*G*height)**.5)
    total_range=math.ceil(total_range)
    x_0=pd.DataFrame([range(total_range)])
    y_0=height-(G/2)*((x_0)/(V*math.cos(theta)))**2 +x_0*math.tan(theta)
    
    x_0=pd.Series(x_0.T.iloc[:,0])
    y_0=pd.Series(y_0.T.iloc[:,0])
    #plt.plot(x_0,y_0)
    
    x_drag=[x]
    y_drag=[y]
    
    x_name=str(theta_name)+'_x'
    y_name=str(theta_name)+'_y'
    
    while y>=0:
        
        
        ax=-(Cd/mass)*vx**2
        ay=-G-(Cd/mass)*vx**2

        vx=vx+ax*delt_t
        vy=vy+ay*delt_t
        
        
        x=x+vx*delt_t
        y=y+vy*delt_t
        
        x_drag.append(x)
        y_drag.append(y)
        
    plt.plot(x_drag,y_drag)
    df_x=pd.DataFrame(x_drag,columns=[x_name])
    df_y=pd.DataFrame(y_drag,columns=[y_name])
    df_theta=pd.concat([df_theta,df_x, df_y], axis=1)

    
    return df_theta
for theta in angles:
    df_theta=Trejectory(theta,V,x,y,df_theta)

    
    

    


    

    

    