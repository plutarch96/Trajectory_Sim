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

from matplotlib.patches import Rectangle, Wedge
import pandas as pd
import matplotlib.pyplot as plt
import os
import getpass
import math
import numpy as np
# number of points between -95 and 15 degrees
resoultion=500
angles=list(np.linspace(-95,15,resoultion))
angle_bins=[-95,-85,-75,-65,-55,-45,-35,-25,-15,-5,5,15]

# simulation resolution
delt_t=.001 # (s)

# spray characteristics
height=15 # (ft)


# velocities for each bin
sprinkler_name='TY5251'
Velocities=[16,14,14,14,14,12,12,12,14,12,12] # (m/s)
D=1 # (mm)
# Colors for angle bins
colors=['b','r','g','m','c','y','k','b','r','g','m','c','y']

kfactor=11.2
pressure=70

flow=kfactor*(70)**.5

# grate specifications
depth=1 # (in)
bearing_bar_thickness=.1875 # (in)
grate_length=45 # (ft)
grate_spacing=1 # (in)

title_name=sprinkler_name+'_'+str(depth)+'_'+str(bearing_bar_thickness)+'_'+str(grate_spacing)+'_'+str(height)

# Do you want to see the drop paths?
path_plotting=1

# close up of the grate interface
zoom=0
# what distance from sprinkler to focus on
#horizontal_view=[0,10]


# Conversions and initializations
height=height*0.3048
depth=depth/12
grate_length=grate_length*0.3048
grate_spacing=grate_spacing*0.0254
bearing_bar_thickness=bearing_bar_thickness*0.0254
D=D/1000
i=0
h_edge=[0,bearing_bar_thickness]
while i<grate_length:
    i=i+grate_spacing
    h_edge.append(i)
    z=i+bearing_bar_thickness
    h_edge.append(z)


velocity_df=pd.DataFrame([])
def Trejectory(theta,V,x,y,df_theta,len_edge,colr):
    

    theta_name=str(theta)

    theta=(theta*3.141592653/180)
    
    
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
    def calculation(V,x,y):
        vx=V*math.cos(theta)
        vy=V*math.sin(theta)
        while y>=-(depth+1):
            
            
            ax=-(Cd/mass)*vx**2
            ay=-G-(Cd/mass)*vx**2
    
            vx=vx+ax*delt_t
            vy=vy+ay*delt_t
            
            
            x=x+vx*delt_t
            y=y+vy*delt_t
            
            x_drag.append(x)
            y_drag.append(y)
            for n in len_edge:
    
                if (h_edge[n] <= x <= h_edge[n+1]) and (-depth*0.3048 <= y <= 0) :
                   
                    return x_drag, y_drag
                
        return x_drag, y_drag
        
                
    x_drag, y_drag=calculation(V,x,y)
    df_x=pd.DataFrame(x_drag,columns=[x_name])

    df_y=pd.DataFrame(y_drag,columns=[y_name])

    df_xy=pd.concat([df_x, df_y], axis=1)
    df_xy=df_xy*3.28084
    if path_plotting==1:
        plt.plot(df_xy[x_name],df_xy[y_name],linewidth=.5, color=colr)
    
    df_xy=df_xy.loc[df_xy[y_name]<-depth].dropna()
    df_xy=df_xy.dropna(axis='columns',how='all')
    
    df_theta=pd.concat([df_theta,df_xy], axis=1,ignore_index=False)

    return df_theta, total_range



    

x=0
y_max=0
total_range=0
len_edge=list(range(0,len(h_edge),2))
  
y=height
G=9.80665
mass=(4/3)*(3.141592653)*((D/2)**3)*(1000)
rho=1.225
A=(3.141592653*(D/2)**2)
Cd=rho*.45*A/2
if path_plotting==1:
    fig, ax = plt.subplots()
df_theta=pd.DataFrame([])

    
for theta in angles:
    for n in range(0,len(angle_bins)-1):
        
        if theta>=angle_bins[n] and theta<=angle_bins[n+1]:
            colr=colors[n]
            V=Velocities[n]
        
            df_theta,total_range=Trejectory(theta,V,x,y,df_theta,len_edge,colr)
    
    
clear_angles=list(df_theta.columns.values)
clear_angles=[x for x in clear_angles if not 'x' in x]

clear_angles=[s.replace("_y", "") for s in clear_angles]
clear_angles=[float(x) for x in clear_angles]
if zoom==1:
    plt.ylim([-.5,.25])
    

if path_plotting==1:
    ax.axhline(y=0,xmin=0, xmax=1.0,color='black')
    ax.axhline(y=-depth,xmin=0.0, xmax=1.0,color='black')  
    plt.title(title_name)


plt.figure()
plt.hist(clear_angles, resoultion, facecolor='green', alpha=0.5)
plt.title(title_name)
plt.xlabel('Initial Angle')

clear_angles=pd.DataFrame(clear_angles,columns=[str(V)+' (m/s)'])

velocity_df=pd.concat([velocity_df,clear_angles],axis=1)



    

    

    
