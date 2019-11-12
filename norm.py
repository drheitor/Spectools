#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:20:50 2019

@author: Heitor
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models
from astropy import units as u
from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_generic_continuum
from scipy.interpolate import interp1d

#--------------------------------


INPUT_spec= 'apStar-r8-2M18282921-1641112.txt'

FILENAME= INPUT_spec[0:28]+'norm.txt'

wl,fl = np.genfromtxt(INPUT_spec, unpack=True)


spectrum = Spectrum1D(flux=fl*u.Jy, spectral_axis=wl*u.AA)

g1_fit = fit_generic_continuum(spectrum)
y_continuum_fitted = g1_fit(wl*u.AA)

#add a spline with a selected dots 

#--------------------------------

f0=plt.figure(figsize=(12,7))
ax0 = f0.add_subplot(111)

ax0.plot(wl, fl)
ax0.set_title('Continuum Fitting')
ax0.grid(True)

point = plt.ginput(n=0, timeout=0, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2)


xn=[]
yn=[]
n=0
for i in point:
    xn.append(point[n][0])
    yn.append(point[n][1])
    n=n+1
    
#--------------------------------

f = interp1d(xn,yn, kind='cubic')
xnew = np.linspace(wl[0], wl[-1], num=len(wl)*10, endpoint=True)


#g1_fit = fit_generic_continuum(spectrum)
#continum = g1_fit(wl*u.AA)

#--------------------------------


f1=plt.figure(figsize=(12,7))
ax1 = f1.add_subplot(111)

ax1.plot(wl, fl)
ax1.set_title('Continuum Fit')
#ax1.plot(wl, y_continuum_fitted)
#ax1.plot(spec_normalized.spectral_axis, spec_normalized.flux)
ax1.plot(wl,f(wl))
f1.savefig('fit-'+FILENAME+'.pdf')


#--------------------------------

continum = f(wl)

spec_normalized = spectrum / continum

f2=plt.figure(figsize=(12,7))
ax2 = f2.add_subplot(111)
ax2.plot(spec_normalized.spectral_axis, spec_normalized.flux)
ax2.set_title('Continuum normalized spectrum')
ax2.grid('on')
f2.savefig('normspec-'+FILENAME+'.pdf')



pfil = open(FILENAME, 'w')
pfil.write('# Wavelenght Flux \n')
  
n=0   
for i in spec_normalized.flux.value:
    flu  = float(i)
    wave = float(spec_normalized.spectral_axis[n].value)
    pfil.write('%7.4f %10.5f\n'%(wave,flu))     
    n=n+1









