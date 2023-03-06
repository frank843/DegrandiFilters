# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 13:50:15 2022

@author: Frank De Grandi
"""

from wavsoftdenoise import logfile
from fdwt import fdwt

# wavelet transform in the log domain, 4 levels
def wavtransform(dir, file, wavdir, wavfile, dp, dl, nodwt):
    if (nodwt == 0):
        logfile(dir, file, wavdir, file+'_log', dp, dl)
        fdwt(wavdir, file+'_log', wavdir, wavfile, 4, dp, dl)
        
def wavtransformLin(dir, file, wavdir, wavfile, dp, dl, nodwt):
    if (nodwt == 0):
        fdwt(dir, file, wavdir, wavfile, 4, dp, dl)

        