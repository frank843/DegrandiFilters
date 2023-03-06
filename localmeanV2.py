# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:37:12 2022

@author: Frank De Grandi
"""
from wavsoftdenoise import logfile
from fdwt import fdwt
from noiseEst import homoarea
from wavthr import findthr
from wavsoftdenoise import wavthreshold

def localmeanV2(dir, file, wavdir, wavfile, xmin, ymin, dp, dl):
    print('finding wavelet coefficients thresholds')
    thr=findthr(wavdir, file+'_log', wavdir, wavfile , dp, dl, xmin, ymin)
    thrwx = thr[0]
    thrwy = thr[1]
    print('threshold wavelet coefficients')
    wavthreshold(wavdir, wavfile, wavdir, dp, dl, thrwx, thrwy)
    
    

   
    