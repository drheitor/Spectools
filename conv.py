#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 21:31:00 2019

@author: Heitor
"""

from specutils import Spectrum1D
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
from specutils.manipulation import (box_smooth, gaussian_smooth, trapezoid_smooth)
from astropy.convolution import Gaussian1DKernel, convolve


INPUT_spec= 'CS31_CNO_0n.spec'


fwhm=0.20
#SIGMA=8


SIGMA=fwhm/2.35482 *100

wl,fl = np.genfromtxt(INPUT_spec, skip_header=2, unpack=True)

wl2,fl2 = np.genfromtxt('fluxCS31_0.norm.nulbad.0.200', skip_header=2, unpack=True)



spec1 = Spectrum1D(spectral_axis=wl * u.A, flux=fl * u.Jy)


#spec1_tsmooth = trapezoid_smooth(spec1, width=3)
#spec1_bsmooth = box_smooth(spec1, width=3)
#spec1_msmooth = median_smooth(spec1, width=3)

spec1_gsmooth = gaussian_smooth(spec1, stddev=SIGMA)


g = Gaussian1DKernel(stddev=SIGMA)
# Convolve data
z = convolve(fl, g)




#plt.plot(spec1.spectral_axis, spec1.flux)

plt.plot(wl2,fl2)
plt.plot(wl,z)
#plt.plot(spec1_gsmooth.spectral_axis, spec1_gsmooth.flux)




#snr_threshold(spectrum, value[, op])
