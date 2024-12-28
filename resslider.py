#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 14:25:55 2024

@author: heitor
"""

#turbospectrum
from __future__ import annotations
try:
    from scripts_for_plotting import *
except ModuleNotFoundError:
    import sys
    sys.path.append('/Users/heitor/Desktop/NLTE-code/TSFitPy/')
    from scripts_for_plotting import *
 
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import seaborn as sns
import csv
import sys

from scipy.interpolate import interp1d
from scipy.optimize import minimize

from numpy.polynomial.chebyshev import Chebyshev
from scipy.ndimage import gaussian_filter1d

from matplotlib.widgets import Slider

from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_style("white")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 1.5})



turbospectrum_paths = {"turbospec_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/turbospectrum/exec-gf/",  # change to /exec-gf/ if gnu compiler
                       "interpol_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/scripts/model_interpolators/",
                       "model_atom_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/input_files/nlte_data/model_atoms/",
                       "departure_file_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/input_files/nlte_data/",
                       "model_atmosphere_grid_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/input_files/model_atmospheres/",
                       "line_list_path": "/Users/heitor/Desktop/NLTE-code/TSFitPy/input_files/linelists/linelist_for_fitting_MY/"}



    
def update(val):
    v_offset = slider_vert.val
    h_offset = slider_horiz.val
    
    # Update observed spectrum position
    obs_line.set_ydata(observed + v_offset)
    obs_line.set_xdata(wavelength_observed + h_offset)
    
    # Recompute residuals dynamically using Template 00
    shifted_template = np.interp(wavelength_observed + h_offset, wavelength_000, flux_000)
    residuals = (observed + v_offset) - shifted_template
    res_line.set_ydata(residuals)
    res_line.set_xdata(wavelength_observed + h_offset)
    
    # Synchronize x-axis for both panels
    ax.set_xlim(lmin, lmax)
    ax_residuals.set_xlim(lmin, lmax)
    fig.canvas.draw_idle()


def turbo(teff,logg,met,vmic,lmin,lmax,FWHM,al_abond):
    
    print('=====================================================================')
    
    #teff = 5500
    #logg = 4.0
    #met = -1.0
    #vmic = 1.0
    
    #lmin = 4600
    #lmax = 5500

    ldelta = 0.01
    
    atmosphere_type = "1D"   # "1D" or "3D"
    nlte_flag = False
    
    elements_in_nlte = ["Al"]  # can choose several elements, used ONLY if nlte_flag = True
    element_abundances = {"Al": al_abond, "Ca": -0.15}  # elemental abundances [X/Fe]; if not written solar scaled ones are used
    include_molecules = False  # way faster without them
    
    # plots the data, but can also save it for later use
    wavelength, flux = plot_synthetic_data(turbospectrum_paths, teff, logg, met, vmic, lmin, lmax, ldelta, atmosphere_type, nlte_flag, elements_in_nlte, element_abundances, include_molecules, resolution=0, macro=0, rotation=0, verbose=False)

    #convolution

    #FHWM (0.12A = 12 pixels) = 2.354 * sigma = 2.354 * 5.09 pixels
    #FWHM= 0.12
    
    pix = FWHM/ldelta

    sig= pix/2.354

    z = gaussian_filter1d(flux, sigma=sig)
    
    print('=====================================================================')

    
    return wavelength, z



INCSV='../out/norm/HD-120559_390_summed_spectrum_normalized_spectrum_p2.csv'
#OUTCSV=INCSV[:-4]+'...'

s = pd.read_csv(INCSV,sep=',')

print(s.keys())


#----------------------------------------------------------


#turbo standard parameters
teff = 5486
logg = 4.58

met = -0.91

vmic = 1.05

lmin = 3920
lmax = 3990



#ldelta = 0.01
FWHM= 0.07


#check
#BD-01-306
#Star,Teff,logg,[Fe/H]1D,Vturb
#BD-21 3420,5909,4.3,-1.14,1.12

#HD120559,5486,4.58,-0.91,1.05


al_abond=-99
wavelength_nan, flux_nan = turbo(teff,logg,met,vmic,lmin,lmax,FWHM,al_abond)


al_abond=-1.0
wavelength_m10, flux_m10 = turbo(teff,logg,met,vmic,lmin,lmax,FWHM,al_abond)

al_abond=-0.1
wavelength_000, flux_000 = turbo(teff,logg,met,vmic,lmin,lmax,FWHM,al_abond)

al_abond=0.5
wavelength_p10, flux_p10 = turbo(teff,logg,met,vmic,lmin,lmax,FWHM,al_abond)

#----------------------------------------------------------


# Example data (replace with your actual data)
wavelength_observed = s['wave']  # Observed wavelength
observed = s['flux']

wavelength_template = wavelength_m10 # Template wavelength
template = flux_m10



# Create the main plot and the residuals panel
fig, (ax, ax_residuals) = plt.subplots(
    2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]}
)
plt.subplots_adjust(bottom=0.3, hspace=0.05)

# Plot the observed spectrum
obs_line, = ax.plot(wavelength_observed, observed,'x', label="Observed", color="black", lw=1.5)

# Plot multiple templates
temp_line1, = ax.plot(wavelength_nan, flux_nan, label="NaN", color="gray", lw=1.5)

temp_line2, = ax.plot(wavelength_m10, flux_m10, label="m10", color="red", lw=1.8,alpha=0.3)
temp_line3, = ax.plot(wavelength_000, flux_000, label="00", color="red", lw=1.8,alpha=1.0)
temp_line4, = ax.plot(wavelength_p10, flux_p10, label="p10", color="red", lw=1.8,alpha=0.3)

# Compute and plot residuals (initially using Template 1)
residuals = observed - np.interp(wavelength_observed, wavelength_000, flux_000)
res_line, = ax_residuals.plot(wavelength_observed, residuals, color="black", lw=1.5)

# Set labels and legend
#ax.set_xlabel("Wavelength (Å)")
ax.set_ylabel("Flux")
ax.legend(loc="upper right")
ax_residuals.set_ylabel("Residuals")
ax_residuals.set_xlabel("Wavelength (Å)")

# Link x-axis of both panels
ax_residuals.set_xlim(ax.get_xlim())
ax_residuals.axhline(0, color="gray", linestyle="--", lw=1)



# Sliders
ax_vert = plt.axes([0.2, 0.2, 0.65, 0.03])
ax_horiz = plt.axes([0.2, 0.15, 0.65, 0.03])

ax.set_xlim(lmin, lmax)
ax_residuals.set_xlim(lmin, lmax)
ax_residuals.set_ylim(-0.35, 0.35)

slider_vert = Slider(ax_vert, "Vertical Offset", -1.0, 1.0, valinit=0.0)
slider_horiz = Slider(ax_horiz, "Horizontal Offset", -50, 50, valinit=0.0)

# Connect sliders to update function
slider_vert.on_changed(update)
slider_horiz.on_changed(update)

plt.show()
