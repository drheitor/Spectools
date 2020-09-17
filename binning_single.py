#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:59:52 2019

@author: Heitor
"""

import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import math 


def Resize(source, length):
    step = float(len(source) - 1) / (length - 1)
    for i in range(length):
        key = i * step
        low = source[int(math.floor(key))]
        high = source[int(math.ceil(key))]
        ratio = key % 1
        yield (1 - ratio) * low + ratio * high

 
    
def save(wl,fl,NAME):
    FNAME=NAME+str(pace)+'.B'
    file = open(FNAME, 'w')
    file.write(NAME[12:25]+'\n')
    file.write('# Wavelength(A) Flux \n')
    n=0   
    for i in fl:
        flu  = float(fl[n])
        wave = float(wl[n])
        file.write('%7.5f %10.7f\n'%(wave,flu))     
        n=n+1
    print(NAME+' saved as ' + FNAME)
   
    
#-----------------------------------------

sns.set_style("white")
sns.set_context("paper", font_scale=2.0, rc={"lines.linewidth": 2.5})

#-----------------------------------------

 
INPUT_spec = sys.argv[1]

pace = float(sys.argv[2])

#INPUT_spec ='flux_G_m3_p10.norm.nulbad.0.150'

print('Input file: '+str(INPUT_spec))


#-----------------------------------------
#spectrum 


#CUBES

wl11,flux11 = np.genfromtxt(INPUT_spec, skip_header=2, unpack=True)



#wlfl11 = numpy.delete(wlfl11, (14990), axis=1)
#-----------------------------------------

#REBIN

#CUBES
#pace=0.06
#UVES
#pace=0.03
#10k
#pace=0.12



x= int((wl11[len(wl11)-1]-wl11[0] )/pace)

wl11b=list(Resize(wl11, x))
flux11b=list(Resize(flux11, x))


#-----------------------------------------

plt.plot(wl11,flux11, 'k')
plt.plot(wl11b, flux11b, 'red')


#-----------------------------------------

#CUBES SAVE
save(wl11b,flux11b,INPUT_spec)
























#-----------------------------------------

