#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:43:34 2024

@author: heitor
"""


from astroquery.simbad import Simbad
import numpy as np

import csv
import pandas as pd



def get_gaia_dr3_ids(star_list):
    """
    Retrieve Gaia DR3 IDs for a list of star names using Simbad.

    Parameters:
    star_list (list of str): List of star names to query.

    Returns:
    list of str: Corresponding Gaia DR3 IDs for the stars.
    """
    gaia_id_list = []  # List to store Gaia DR3 IDs

    # Remove duplicates from the star list
    unique_stars = list(set(star_list))

    for star in unique_stars:
        # Query Simbad for object IDs
        ids = Simbad.query_objectids(star)

        # Initialize Gaia DR3 ID as NaN
        gaia_id = np.nan

        if ids is not None:
            # Search for Gaia IDs in the queried results
            for identifier in ids:
                if 'Gaia DR3' in identifier[0]:
                    gaia_id = identifier[0]
                    break  # Stop searching once Gaia DR3 ID is found

        gaia_id_list.append(gaia_id)

    return gaia_id_list




# Example usage
if __name__ == "__main__":
    # Replace with your actual list of star names
    star_names = ["HD 103723", "BD+02 2541"]  # Example list
    
    INCSV='~/Desktop/simbad-id-45ASA.csv'
    #OUTCSV=INCSV[:-4]+'...'

    s = pd.read_csv(INCSV,sep=';')
    
    
    star_names = list(s['simbad-ID'])
    

    # Get Gaia DR3 IDs
    gaia_ids = get_gaia_dr3_ids(star_names)

    # Print results
    print("Gaia DR3 IDs:", gaia_ids)



























































#