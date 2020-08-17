#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:13:45 2018

@author: Heitor
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation



#ids,rvmiles,rvcoelho,dif = np.genfromtxt('MUSEter9-RV.txt', skip_header=1, unpack=True, dtype='unicode')

#ids_ca,rvmiles_ca,rv_ca,dif_ca = np.genfromtxt('MUSEter9-RV-CaIII.txt', skip_header=1, unpack=True, dtype='unicode')



# keck = EarthLocation.of_site('Keck')  # the easiest way... but requires internet
VLT = EarthLocation.from_geodetic(lat=-24.62704444*u.deg, lon=--70.40395833*u.deg, height=2635.43*u.m)
#Terzan9
sc = SkyCoord(ra=270.41166667*u.deg, dec=-26.83972222*u.deg)

barycorr = sc.radial_velocity_correction(obstime=Time('2016-6-10'), location=VLT)

barycorr.to(u.km/u.s)  
#<Quantity 20.077135 km / s>


heliocorr = sc.radial_velocity_correction('heliocentric', obstime=Time('2016-6-4'), location=VLT)
heliocorr.to(u.km/u.s)  
#<Quantity ￼8.3997245 km / s>