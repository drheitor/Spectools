#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:54:34 2019

@author: Heitor
"""

import numpy as np 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import seaborn as sns
from matplotlib.widgets import RectangleSelector, Button, Slider
from matplotlib.widgets import TextBox

sns.set_style("white")
sns.set_context("paper", font_scale=2.0, rc={"lines.linewidth": 2.5})


#---------------------------------------------------
#  DEF


def norma(flux,wl,norm_a):
    n=0
    while n < len(wl1):
        if wl[n] > lamb_1-1 and wl[n] < lamb_1+1:
            norm_1=flux[n]
        n=n+1
    try:    
        return flux/(norm_1+norm_a)
    except:
        raise Exception('Check the wavelenght of the the observed spectrum')
        
        
def norma2(flux,wl,norm_a):
    n=0
    while n < len(wl1):
        if wl[n] > lamb_2-1 and wl[n] < lamb_2+1:
            norm_2=flux[n]
        n=n+1
   
    
    return flux/(norm_2+norm_a)

    
    


def rvcorr(wl,rv):
    return wl+rv

#---------------------------------------------------
#observ2

INPUT_Obs='./spec-obs/89848_moyen_l_ncg4.dat'

#INPUT_Obs='./spec-obs/89848_moyen_l_ncg4.dat'


# 393125_moyen_l_ncg4.dat 01
# 545749_moyen_l_ncg4.dat 02
# 564840_moyen_l_ncg4.dat 03
# 564857_moyen_l_ncg4.dat 04
# 575542_moyen_l_ncg4.dat 05

# 78255_moyen_l_ncg4.dat 08
# 78271_moyen_l_ncg4.dat 09
# 89589_moyen_l_ng.dat 10
# 89735_moyen_l_ng.dat 11
# 89832_moyen_l_ng.dat 12
# 89848_moyen_l_ng.dat 13


#---------------------------------------------------    

#linelist
#copper
lamb=[5105.5374,5218.1974]

#cobalt
#lamb=[5212.691,5280.629,5301.047,5342.708,5454.572,5647.234,6117.000,6188.996]


starname='BWc13'

#number of the plot
n=0

#starts with 0
lamb_1=lamb[0]

lamb_2=lamb[1]

OUTPUT=['./figs/'+starname+'Cu-'+str(n)+'.pdf']

#---------------------------------------------------
#1

ylim_1=[0.1,1.1]

conv1='0.160'
    
norm_a1= 0.49

rv1= -0.01

#---------------------------------------------------
#2

ylim_2=[0.2,1.1]

conv2='0.200'

norm_a2= 0.14

rv2= -0.03


#---------------------------------------------------
#

SYN1='./flux/flux'+starname+'0.norm.nulbad.'+conv1

SYN2='./flux/flux'+starname+'03.norm.nulbad.'+conv1

SYN3='./flux/flux'+starname+'m03.norm.nulbad.'+conv1



SYN12='./flux/flux'+starname+'0.norm.nulbad.'+conv2

SYN22='./flux/flux'+starname+'03.norm.nulbad.'+conv2

SYN32='./flux/flux'+starname+'m03.norm.nulbad.'+conv2



#---------------------------------------------------

# open spectrum


wl1,flux1 = np.genfromtxt(INPUT_Obs, skip_header=2, unpack=True)


#-----------

wl11,flux11 = np.genfromtxt(SYN1, skip_header=2, unpack=True)

wl21,flux21 = np.genfromtxt(SYN2, skip_header=2, unpack=True)

wl31,flux31 = np.genfromtxt(SYN3, skip_header=2, unpack=True)


wl12,flux12 = np.genfromtxt(SYN12, skip_header=2, unpack=True)

wl22,flux22 = np.genfromtxt(SYN22, skip_header=2, unpack=True)

wl32,flux32 = np.genfromtxt(SYN32, skip_header=2, unpack=True)


#---------------------------------------------------

#interpolation

#flux_new = flux / a
#flux2_new = flux2


#f = interp1d(wl, flux_new, kind="cubic")

#wlnew = np.linspace(min(wl), max(wl), num=10000, endpoint=True)

#ax1.plot(wlnew,f(wlnew),linewidth=1.7, label='APOGEE')


#---------------------------------------------------

#plot

#plt.figure(1)

f1 = plt.figure(figsize=(10,8))


ax1 = f1.add_subplot(211)

#f1.subplots_adjust(left=0.15, bottom=0.25)

ax1.plot(rvcorr(wl1,rv1),norma(flux1,wl1,norm_a1),linewidth=1.0, ls='--', label='obs',color='black')

ax1.plot(wl11,flux11,linewidth=1.5, label='SYN',color='red')
ax1.plot(wl21,flux21,linewidth=1.5, label='SYN',color='red')
ax1.plot(wl31,flux31,linewidth=1.5, label='SYN',color='red')
ax1.axvline(x=lamb_1, linewidth=0.5, color='k', ls='--')

#ax1.legend(loc=2)
ax1.set_title(starname)
#ax1.set_xlabel('Wavelength ( $\AA$ )')
ax1.set_ylabel('Arbritrary Flux')
ax1.set_xlim([lamb_1-1,lamb_1+1])
ax1.set_ylim(ylim_1)

#-------------


ax2 = f1.add_subplot(212)

#f1.subplots_adjust(left=0.15, bottom=0.25)

ax2.plot(rvcorr(wl1,rv2),norma2(flux1,wl1,norm_a2),linewidth=1.0,ls='--', label=starname,color='black')

ax2.plot(wl12,flux12,linewidth=1.5, label='SYN',color='red')
ax2.plot(wl22,flux22,linewidth=1.5, label='SYN',color='red')
ax2.plot(wl32,flux32,linewidth=1.5, label='SYN',color='red')
ax2.axvline(x=lamb_2, linewidth=0.5, color='k', ls='--')

#ax1.legend(loc=2)
ax2.set_xlabel('Wavelength ( $\AA$ )')
ax2.set_ylabel('Arbritrary Flux')
ax2.set_xlim([lamb_2-1,lamb_2+1])
ax2.set_ylim(ylim_2)


plt.show()

f1.savefig(OUTPUT[0])



#---------------------------------------------------








