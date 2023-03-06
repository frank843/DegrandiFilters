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

def localmean(dir, file, wavdir, wavfile, dp, dl, nodwt):
    
    logfile(dir, file, wavdir, file+'_log', dp, dl)
    if (nodwt == 0):
        fdwt(wavdir, file+'_log', wavdir, wavfile, 4, dp, dl)
    blockpos=homoarea(wavdir, file+'_log', dp, dl)
    xmin=blockpos[0]
    ymin=blockpos[1]
    thr=findthr(wavdir, file+'_log', wavdir, wavfile , dp, dl, xmin, ymin)
    thrwx = thr[0]
    thrwy = thr[1]
    wavthreshold(wavdir, wavfile, wavdir, dp, dl, thrwx, thrwy)
    print('end of job')
    

   
    