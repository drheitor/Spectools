#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:07:03 2019

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
    while n < len(wl):
        if wl[n] > lamb_1-1 and wl[n] < lamb_1+1:
            norm_1=flux[n]
        n=n+1

    try:    
        return flux/(norm_1+norm_a)
    except:
        raise Exception('Check the wavelenght of the observed spectrum')


def rvcorr(wl,rv):
    return wl+rv


    
def update(val):
    norm_a=norm_slider
    f = norma(flux1,wl1,norm_a)
    ax1.set_ydata(f)
    
    ax1.draw()

#---------------------------------------------------
#observ
    

INPUT_Obs='./spec-obs/89848_moyen_l_ncg4.dat'

#INPUT_Obs='./spec-obs/89848_moyen_l_ncg4.dat'




#---------------------------------------------------    

#linelist

lamb=[5105.5374, 5218.1974]

#lamb=[5212.691,5280.629,5301.047,5342.708,5454.572,5647.234,6117.000,6188.996]
  

starname='BWc13'


conv='0.200'
    
lamb_1=lamb[1]


norm_a= 0.51

rv= 0.0


#---------------------------------------------------    

#local variable 'norm_1' referenced before assignment

OUTPUT=[starname+str(lamb_1)+'-Cu.pdf']

#---------------------------------------------------    


SYN1='./flux/flux'+ starname+'0.norm.nulbad.'+conv

SYN2='./flux/flux'+starname+'03.norm.nulbad.'+conv

SYN3='./flux/flux'+starname+'m03.norm.nulbad.'+conv




#---------------------------------------------------

# open spectrum


wl1,flux1 = np.genfromtxt(INPUT_Obs, skip_header=2, unpack=True)


#-----------

wl11,flux11 = np.genfromtxt(SYN1, skip_header=2, unpack=True)

wl21,flux21 = np.genfromtxt(SYN2, skip_header=2, unpack=True)

wl31,flux31 = np.genfromtxt(SYN3, skip_header=2, unpack=True)


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

axis_color = 'lightgoldenrodyellow'


f1 = plt.figure(figsize=(12,6))


ax1 = f1.add_subplot(111)

f1.subplots_adjust(left=0.15, bottom=0.25)


[line] = ax1.plot(rvcorr(wl1,rv),norma(flux1,wl1,norm_a),linewidth=1.5, label=starname,color='black')
ax1.plot(wl11,flux11,linewidth=1.5, label='SYN',color='red')
ax1.plot(wl21,flux21,linewidth=1.5, label='SYN',color='red')
ax1.plot(wl31,flux31,linewidth=1.5, label='SYN',color='red')
ax1.axvline(x=lamb_1, linewidth=0.5, color='k', ls='--')

#ax1.legend(loc=2)
ax1.set_title(starname)
ax1.set_xlabel('Wavelength ( $\AA$ )')
ax1.set_ylabel('Arbritrary Flux')
ax1.set_xlim([lamb_1-1,lamb_1+1])
ax1.set_ylim([0.1,1.1])

# Draw another slider
norm_slider_ax = f1.add_axes([0.15, 0.1, 0.55, 0.03], facecolor=axis_color)
norm_slider = Slider(norm_slider_ax, 'Norm', -1.5, 2.5, valinit=norm_a)

# Define an action for modifying the line when any slider's value changes
def sliders_on_changed(val):
    line.set_ydata(norma(flux1,wl1,norm_slider.val))
    f1.canvas.draw_idle()
    norm_a=norm_slider.val
norm_slider.on_changed(sliders_on_changed)
norm_slider.on_changed(sliders_on_changed)

# Draw another slider
rv_slider_ax = f1.add_axes([0.15, 0.05, 0.55, 0.03], facecolor=axis_color)
rv_slider = Slider(rv_slider_ax, 'RV', -4.5, 4.5, valinit=rv)

# Define an action for modifying the line when any slider's value changes
def sliders_on_changed(val):
    line.set_xdata(rvcorr(wl1,rv_slider.val))
    f1.canvas.draw_idle()
    rv=rv_slider.val
rv_slider.on_changed(sliders_on_changed)
rv_slider.on_changed(sliders_on_changed)



# Add a button for resetting the parameters
reset_button_ax = f1.add_axes([0.8, 0.1, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
def reset_button_on_clicked(mouse_event):
    norm_slider.reset()
    rv_slider.reset()
reset_button.on_clicked(reset_button_on_clicked)


# Add a button for resetting the parameters
Quit = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), ' Close ', color="red")
def close(event): plt.close()
Quit.on_clicked(close)

#plt.subplots_adjust(wspace=0.15)

plt.show()

#f1.savefig(OUTPUT[0])








