#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 14:23:07 2023

@author: heitorernandes
"""

import numpy as np
from pypdf import PdfMerger
import os
import sys


#IN='*.pdf'


IN = sys.argv[1]

#print(IN)
# include something like this '*15*.pdf' with ''

os.system('ls ' +IN+ ' > allpdfs')



pdfs = np.genfromtxt('allpdfs', dtype=str)
#pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']


print('Saving the plots...')
merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("Combined.pdf")
merger.close()

print('----DONE----')
print('------------')







