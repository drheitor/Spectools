#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 08:45:31 2018

@author: Heitor
"""

import numpy as np
import os 



INPUT= 'MUSEter9-RV-CaT.txt'



os.system('ls *.ascii > list')



ID, rvmiles, rvCaT, ratio  = np.genfromtxt(INPUT, skip_header=1, unpack=True, dtype='unicode')

listin = np.genfromtxt('list', dtype='unicode')


wlnew2=[]

n=0
for spec in listin:
    h=0
    name='rv-'+ spec
    file= open(name , 'w') 
    wlspec,flux = np.genfromtxt(spec, skip_header=1, unpack=True)
    m=len(flux)
    file.write(str(m) + '\n')

    for wl in wlspec:
        dwl=(float(rvCaT[n])/299792.458)*wl
        wlnew=wl-dwl
        fluxx=flux[h]
        file.write('%7.7f  %7.7f \n'%(wlnew, fluxx))
        wlnew2.append(wlnew)
        h=h+1
        
    n=n+1
    

    
    
    

