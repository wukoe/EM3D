# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 15:44:28 2016
data process for image
@author: wubia
"""
import matplotlib.pyplot as plt
import numpy as np

mxr=(260,203,203)

def show(R,xidx):
    I=(R[:,2]==xidx[0])&(R[:,3]==xidx[1])
    v=np.zeros(mxr)
    a=R[I]
    for k in a:
        v[k[0],k[1]]=1    
    plt.imshow(v)
    plt.show()
    return I
    
def seproi(R,xidx):
    I=show(R,xidx)
    a=R[I]
    # max of range in Z and Y
    imax=np.max(a[:,:2],0)
    imin=np.min(a[:,:2],0)
    fidx=[imin[0],imax[0],imin[1],imax[1],xidx[0],xidx[1]]
    return (fidx,I)
    
def uproi(R,I):
    a=np.array([k for k in range(len(I))])    
    return np.delete(R,a[I],0)
    
    
def proc(R,F):
    while len(R)>0:
        a=R[0,2:4]
        fidx,I=seproi(R,a)
        
        print([sum(I),len(R)])
        if sum(I)==0:
            break
        input("Press Enter to continue...")
        F.append(fidx)
        R=uproi(R,I)
        
    return F,R
    
def tp(R):
    v=np.zeros(mxr)
    for z in range(46,250):        
        I=R[:,0]==z
        a=R[I]
        for k in range(len(a)):
            v[z,a[k,1],a[k,2]:a[k,3]]=1
    return v