# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 15:31:30 2022

@author: Frank DE Grandi
"""


from wavtrans import wavtransform
from wavtrans import wavtransformLin
from coherNoiseEst import cohernoiseEst
from coherNoiseEst import wasthrEstimCC
from wavsoftdenoiseCC import wavthresholdCC

# dir: imput data set directory
# file: input data set (must be float32 ENVI 4 data type)
# wavdir: directory for wavelet data representation
# outfile: filetered data set
# dp: number of pixel in the input datat set
# dl: number of lines in the input data set
# skipdwt: switch set to 1 to skip the wavelet transform step
# linsw: set to one to prerform filtering in the linear domain


def specklekillerCC(dir, file, wavdir, outdir, outfile, dp, dl, skipdwt, linsw):
    nj=4
    if (linsw == 1):
        wavtransformLin(dir, file, wavdir, outfile, dp, dl, skipdwt)
    else:
    # wavelet reansform in the log domain
        wavtransform(dir, file, wavdir, outfile, dp, dl, skipdwt)
    # estimation of the linear fit coeficients of the wx and wy wavelets
    print('estimate linear fit of wavelet coefficients and backscatter')
    rw=cohernoiseEst(dir, file, outfile, wavdir, nj, dp, dl)
    rwx=rw[0]
    rwy=rw[1]
      
    print('generate thresholdeds for wx and wy')
    wasthrEstimCC(wavdir, outfile, rwx, rwy, dp, dl)
    
# compute the thresholded and smoothed wavelet coefficients
# invert DWT and recontruct the local mean value image
    print('threshold wavelet coefficients and invert wavelet transform')
    
    wavthresholdCC(wavdir, outfile, outdir, dp, dl, 0)
    
