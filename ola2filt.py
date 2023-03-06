# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 18:56:00 2022

@author: Frank De Grandi
"""
from scipy.signal import sepfir2d
import numpy as np

from logfile import logfile


def test():
    h1 = np.array([0.0, 0.0, 0.125, 0.375, 0.375, 0.125, 0.0], dtype='float32')
    # h2=np.array([0.0, 0.0, 0.0, -2.0, 2.0, 0.0,  0.0], dtype='float32')
    h2 = h1
    inf="O:/sentinel/timeseries/ENVI/setA0CA_rsp_float_log"
    outf="O:/sentinel/timeseries/ENVI/setA0CA_test"
    dir='O:/sentinel/timeseries/ENVI'
    dp=26706
    dl=16889
    logfile(dir,  'setA0CA_rsp_float', dir, 'setA0CA_rsp_float_log', dp, dl)
    ola2filt(inf, outf, dp, dl, h1, h1 )

def ola2filt(infile, outfile, dp, dl, h1, h2):
    bs=512
    fs=h1.size
    nb = int(dl/bs)
    # rem = dl % bs
    rem = dl - nb * bs
    print('ola n, rem', nb, rem)
    nrlines=0
    outbl=bs
    froutbl=bs-fs
# work buffer
    wrkbl=bs+2 * fs
    fwrkbl=bs
    inwin=np.ones([bs, dp], dtype='float32')
    inwinp=np.ones([bs, dp], dtype='float32')
    inwinlast=np.ones([rem, dp], dtype='float32')
    froutb=np.ones([froutbl, dp], dtype='float32')
    outb=np.ones([outbl, dp], dtype='float32')
    outblast=np.ones([rem+fs, dp], dtype='float32')
    wrkb=np.ones([wrkbl, dp], dtype='float32')
    frwrkb=np.ones([bs, dp], dtype='float32')
    wrkblast=np.ones([2*fs+rem, dp], dtype='float32')
    byl=4
    if (rem != 0):
        nl=froutbl+(nb-1)*outbl+rem+fs
    else:
        nl=froutbl+nb*outbl
    f = open(infile, "rb")
    fout = open(outfile, "wb")
# first step, read inwin, transfer to firstwrkbuf
    
    buf=np.fromfile(f, dtype='float32', count=dp*bs)
    buf[np.isnan(buf)]=0.0
    inwin=buf.reshape(bs, dp)
    frwrkb=sepfir2d(inwin, h1, h2)
    #; only bs-fs lines are output since the last fs lines are convolved only with partial filter
    froutb=frwrkb[0:froutbl, 0:dp]
    fout.write(froutb.reshape(dp*froutbl))
    nrlines=bs
    
    


# save the first input window into inwinp (former window)
    inwinp=inwin
#  step n+1
# ; process the remaining nb-2 blocks if rem ne 0 (since the last one is handled separately
# else process nb-1 blocks

    if (rem != 0):
        nbrem=nb-1
    else: nbrem=nb
    print('nbrem ', nbrem)
    for kk in range(nbrem):
   # read next sliding window
       # print("Ola Step :", kk+2)
       buf=np.fromfile(f, dtype='float32', count=dp*bs)
       buf[np.isnan(buf)]=0.0
       inwin=buf.reshape(bs, dp)
       # ; load into the beginning of wrk buffer the last 2fs lines from the saved previous window
       wrkb[0:2*fs, 0:dp]=inwinp[bs-2*fs:bs, 0:dp]
   # load he remaing lines in wrkbuf with the new window
       wrkb[2 * fs: wrkbl, 0:dp]=inwin
   # convolv the wrkbuf by lines and cols
       cbuf=sepfir2d(wrkb, h1, h2)
       outb = cbuf[fs:fs+outbl, 0:dp]
       # outdata=np.reshape(outb[fs:fs+outbl, 0:dp],dp*outbl)
       fout.write(outb)
       nrlines=nrlines+bs
       inwinp=inwin
       
       


# last step if rem ne 0
    if (rem != 0):
        #print("Last step")
        buf=np.fromfile(f, dtype='float32', count=dp*rem)
        buf[np.isnan(buf)] = 0.0
        inwinlast=buf.reshape(rem, dp)
        wrkblast[0:2*fs, 0:dp]=inwinp[bs-2*fs:bs, 0:dp]
        wrkblast[2*fs:2*fs+rem, 0:dp]=inwinlast
        wrkblastconvol=sepfir2d(wrkblast, h1, h2)
        #outblast=wrkblastconvol[fs:2*fs+rem, 0:dp]
        outblast=wrkblastconvol[fs:, 0:dp]
        # fout.write(outblast.reshape(dp*(rem+fs)))
        fout.write(outblast)
        nrlines=nrlines+rem+fs
    print("lines: ", nrlines)
    fout.close()
    f.close()



    
         

    
   
   


    
