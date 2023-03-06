# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 15:31:30 2022

@author: Frank De Grandi
"""

from localmeanV2 import findthr

from wavtrans import wavtransform
from noiseEst import homoarea
from wavsoftdenoise import  wavthreshold

# dir: imput data set directory
# file: input data set (must be float32 ENVI 4 data type)
# wavdir: directory for wavelet data representation
# outdir: directory of the filteres data set
# outfile: filetered data set
# dp: number of pixel in the input datat set
# dl: number of lines in the input data set
# skipdwt: switch set to 1 to skip the wavelet transform step


def specklekiller(dir, file, wavdir, outdir, outfile, dp, dl, skipdwt):
    
    # wavelet reansform in the log domain
    wavtransform(dir, file, wavdir, outfile, dp, dl, skipdwt)
    # detection of a stationary area with fully developed speckle
    # performed in linear domain
    # fpr log domain file+'/_log' and dir is wavdir
    blockpos=homoarea(wavdir, file+'_log', dp, dl)
    xmin=blockpos[0]
    ymin=blockpos[1]

# estimate wavelet coefficients threshold within the stationay area    
    print('finding wavelet coefficients thresholds')
    thr=findthr(wavdir, file+'_log', wavdir, outfile , dp, dl, xmin, ymin)
    thrwx = thr[0]
    thrwy = thr[1]
    
# compute the thresholded and smoothed wavelet coefficients
# invert DWT and recontruct the local mean value image
    print('threshold wavelet coefficients')
    wavthreshold(wavdir, outfile, outdir, dp, dl, thrwx, thrwy)
    


