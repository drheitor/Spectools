#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:07 2024

@author: heitor
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import sys

from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)



sns.set_style("white")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 1.5})

#---------------





def update_fits_key(file_path, key, new_value):
    
    
    # Open the FITS file in update mode
    with fits.open(file_path, mode='update') as hdul:
        
        # Access the primary header (usually the first header in the HDU list)
        hdr = hdul[0].header
        
        #printing all the keys in the header
        keys = list(hdr.keys())
        print(keys)
        
        # Print the current value of the specified key
        print(f"Current value of '{key}': {hdr.get(key, 'Key not found')}")
        
        # Update the value of the specified key
        hdr[key] = new_value
        
        # Save changes to the FITS file
        hdul.flush()
        
        # Print the updated value to confirm the change
        print(f"Updated value of '{key}': {hdr[key]}")
        
  
        
def read_vhelio_corr(file_path):
    
    
    # Open the FITS file in update mode
    with fits.open(file_path, mode='update') as hdul:
        
        # Access the primary header (usually the first header in the HDU list)
        hdr = hdul[0].header
        
        star = hdr['OBJECT']
        
        key = 'ESO QC VRAD HELICOR'
        
        vhelio_corr = hdr['ESO QC VRAD HELICOR']
        
        # Print the current value of the specified key
        print(f"The '{key}': {vhelio_corr}")
        print("For the star :"+str(star))
        
        return star, vhelio_corr
        
        
        
        
def extract_wavelength_info(file_path):
    # Open the FITS file
    with fits.open(file_path) as hdul:
        # Access the primary header (usually the first header in the HDU list)
        hdr = hdul[0].header
        
        print('---------------')
        print('file:')
        print(file_path)
        
        print('Star: ')
        print(hdr['OBJECT'])
        print('\n')
        
        
        # Get the number of data axes
        num_axes = hdr.get('NAXIS', None)
        if num_axes is None:
            print("NAXIS keyword not found in the FITS header.")
            return None
        
        # Print the number of data axes
        print(f"Number of data axes: {num_axes}")
        
        # Collect axis lengths
        axis_lengths = []
        for i in range(1, num_axes + 1):
            axis_length = hdr.get(f'NAXIS{i}', None)
            if axis_length is None:
                print(f"NAXIS{i} keyword not found in the FITS header.")
                return None
            axis_lengths.append(axis_length)
            print(f"Length of axis {i}: {axis_length}")
        
        # Extract the relevant WCS information
        crval1 = hdr.get('CRVAL1', None)
        cdelt1 = hdr.get('CDELT1', None)
        crpix1 = hdr.get('CRPIX1', None)
        ctype1 = hdr.get('CTYPE1', None)
        cd1_1 = hdr.get('CD1_1', None)
        
        # Print the extracted WCS information
        print(f"CRVAL1: {crval1}")
        print(f"CDELT1: {cdelt1}")
        print(f"CRPIX1: {crpix1}")
        print(f"CTYPE1: {ctype1}")
        print(f"CD1_1: {cd1_1}")
        
        print('---------------')
        
        # Determine the increment (cdelt1 or cd1_1)
        if cd1_1 is not None:
            cdelt1 = cd1_1
        
        # Check if we have enough information to compute the wavelength array
        if crval1 is not None and cdelt1 is not None and crpix1 is not None:
            # Compute the wavelength array
            num_pixels = axis_lengths[0]  # Assuming wavelength is along the first axis (NAXIS1)
            wavelengths = crval1 + (np.arange(num_pixels) + 1 - crpix1) * cdelt1
            return wavelengths
        else:
            print("Not all necessary WCS information is available to compute wavelengths.")
            return None
        
def extract_flux_data(file_path):
    # Open the FITS file
    with fits.open(file_path) as hdul:
        # Print information about the FITS file contents
        hdul.info()
        
        # Access the primary data array (assumed to be the flux data)
        flux_data = hdul[0].data
        
        # If the flux data is in an extension, access it using hdul[ext_number].data
        # For example, if the flux data is in the first extension:
        # flux_data = hdul[1].data
        
        if flux_data is None:
            print("No data found in the primary HDU.")
            return None
        
        # Print some basic information about the flux data
        print(f"Flux data shape: {flux_data.shape}")
        print(f"Flux data type: {flux_data.dtype}")
        
        # If the data is multidimensional, you may want to inspect it or process it further
        # Here we assume it's a 1D array for simplicity
        if flux_data.ndim == 1:
            print("Flux data:", flux_data)
        else:
            print("Flux data is multidimensional. You may need to handle it accordingly.")
        
        return flux_data
        

def rv(centre,centre2):
    dwl=centre-centre2
    wl=centre2
    rv= (dwl*299792.458)/wl
    return rv 



def corrv(wl,flux,rv):
    wlnewl=[]
    for wlp in wl:
        dwl=-(rv/299792.458)*wlp
        wlnew=wlp-dwl
        wlnewl.append(wlnew)
    return [wlnewl,flux]        
        
        
#---------------      
        

# Example usage
#file_path = '../4HE_GSE_AS_sample/HD-219617_564l_OB2.fits'  # Path to your FITS file


file_path = sys.argv[1]  # Path to your FITS file


name_out = file_path[21:-5] + '_helio'

#---------------

#new_value = 'HD 219617'  # The new value for the key
#key = 'OBJECT'             # The header key you want to update


wavelengths = extract_wavelength_info(file_path)



if wavelengths is not None:
    print("Wavelength array:", wavelengths)
    print("length",len(wavelengths))
    print('---------------')



flux_data = extract_flux_data(file_path)



if flux_data is not None:
    print("Flux array:", flux_data)
    print("length",len(flux_data))
    print('---------------')



star, vhelio = read_vhelio_corr(file_path)



new_wv, new_fl = corrv(wavelengths,flux_data,vhelio)

#------------------- plotting ------------------------

fig, axs = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

# Remove horizontal space between axes
fig.subplots_adjust(wspace=0)



axs[0].plot(wavelengths, flux_data, color='gray', label = star)
axs[0].plot(new_wv, new_fl, color='k')



axs[0].set_ylabel('Flux')
axs[0].tick_params(which="both", bottom=True, top=True, left=True, right=True, direction='in')
axs[0].set_xlabel('Wavelength')

#axs[0].set_ylim([-1.5,1.5])
#axs[0].set_xlim([-1.7,0.7])

axs[0].grid()


#axs[0].xaxis.set_major_locator(MultipleLocator(0.5))
#axs[0].xaxis.set_minor_locator(MultipleLocator(0.1))
#axs[0].yaxis.set_major_locator(MultipleLocator(0.5))
#axs[0].yaxis.set_minor_locator(MultipleLocator(0.1))




axs[1].title.set_text("Cutted")

axs[1].plot(wavelengths, flux_data, color='gray', label = star)
axs[1].plot(new_wv, new_fl, color='k')


axs[1].tick_params(which="both", bottom=True, top=True, left=True, right=True, direction='in')
axs[1].set_xlabel('Wavelength')

axs[1].set_xlim([4855,4870])

axs[1].legend(loc=4)

axs[1].grid()

#axs[1].xaxis.set_major_locator(MultipleLocator(0.5))
#axs[1].xaxis.set_minor_locator(MultipleLocator(0.1))
#axs[1].yaxis.set_major_locator(MultipleLocator(0.5))
#axs[1].yaxis.set_minor_locator(MultipleLocator(0.1))



plt.savefig('../fig/helio/Vradhelio-'+name_out+'.pdf')


#---------------------------------------------------


#Saving spectrum

print('\nSaving spectrum: ')
print(name_out)

with open('../out/helio/'+name_out+'.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(new_wv, new_fl))



#---------------------------------------------------






























#