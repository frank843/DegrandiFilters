# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:12:18 2022

@author: Frank DE Grandi
"""

import numpy as np
from fdwt import writehdr

def sigmaToPow(dir, file, outdir, outfile, dp, dl):
    f=open(dir+'/'+file, 'rb')
    fout=open(outdir+'/'+outfile, 'wb')
    for i in range(dl):
        if (i % 100 == 0):
            print(i)
        buf = np.fromfile(f, dtype='float32', count=dp)
        buf = buf.byteswap(inplace=True)
        linePow=np.exp(buf)
        fout.write(linePow)
    fout.close()
    f.close()
    writehdr(outdir, outfile, dp, dl)
    
def sigmaToPow2(dir, file, outdir, outfile, dp, dl):
    f=open(dir+'/'+file, 'rb')
    fout=open(outdir+'/'+outfile, 'wb')
    for i in range(dl):
        if (i % 100 == 0):
            print(i)
        buf = np.fromfile(f, dtype='float32', count=dp)
        buf = buf.byteswap(inplace=True)
        linePow=np.power(10., buf)
        fout.write(linePow)
    fout.close()
    f.close()
    writehdr(outdir, outfile, dp, dl)
    
#sample call
dir='O:/sentinel/sentGeocoded/S1A_20150416_Orb_Cal_ML_Geo.data'
file='Sigma0_VV.img'
outdir=dir+'/powVV'
outfile='pow10VV'
sigmaToPow2(dir, file, outdir, outfile, 12579, 7725)
