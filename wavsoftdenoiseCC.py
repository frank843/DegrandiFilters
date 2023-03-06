# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 17:34:24 2022

@author: Frank De Grandi
"""
import numpy as np

def b3function(xin, m):
    x = xin / float(m)
    ax = abs(x)
    if (ax >= 0.0 and ax < 1):
        b = 2./3.-x ** 2 + 0.5 * ax**3
    else:
        if (ax >= 1.0 and ax < 2.0):
            b = (1./6.) * (2.0 - ax) ** 3
        else:
            b=0.0
    return((1./ float(m)) * b)

def bfilter(m):
    notfound=1
    sup = m
    th = 10. ** -8
    x = float(m)
    while notfound == 1 :
        b = b3function(x, m)
        if (b < th):
            break
        x = x+1.0
        sup = sup+1
    nsup = 2*sup+1
    r = np.ones([nsup], dtype="float32")
    x = np.arange(nsup)-sup
    
    for i in range(nsup):
        r[i]=b3function(x[i], m)
    return(r)


from ola2filt import ola2filt
from invDWT import inDWT

# compute the thresholded and smoothed wavelet coefficients
# invert DWT and recontruct the local mean value image
#
def wavthresholdCC(dirwav, filename, outdir, dp, dl, doexp):
    nj=4
    h = bfilter(4)
    wfilesx=[filename+'_WX1']
    for j in range(nj-1):
        wfilesx=wfilesx+[filename+'_WX'+str(j+2)]
    # print(wfilesx)
    
    wfilesy=[filename+'_WY1']
    for j in range(nj-1):
        wfilesy=wfilesy+[filename+'_WY'+str(j+2)]
        
    # thresholds   
    wfilesTx=[filename+'_TW1_1']
    for j in range(nj-1):
        wfilesTx=wfilesTx+[filename+'_TW1_'+str(j+2)]
    # print(wfilesx)
    
    wfilesTy=[filename+'_TW2_1']
    for j in range(nj-1):
        wfilesTy=wfilesy+[filename+'_TW2_'+str(j+2)]
        
    
    # open each file wx
    for kk in range(nj):
        softfile_wx = wfilesx[kk]+'_sthr'
        f = open(dirwav+'/'+wfilesx[kk], 'rb')
        ft = open(dirwav+'/'+wfilesTx[kk], 'rb')
        fout=open(dirwav+'/tmp.tmp', 'wb')
        for i in range(dl):
            mybuf=np.fromfile(f, dtype='float32', count=dp)
            mythr=np.fromfile(ft, dtype='float32', count=dp)
            iineg=mybuf < 0
            datneg = mybuf[mybuf < 0.0]
            if (iineg.size > 0):
                mybuf=abs(mybuf)
                mybuf = mybuf-mythr
                mybuf[mybuf < 0] = 0
                mybuf[iineg] = - mybuf[iineg]                          
            fout.write(mybuf)
           
        f.close()
        fout.close()
        
        ola2filt(dirwav+'/tmp.tmp', dirwav+'/'+softfile_wx, dp, dl, h, h)
        
        # same for wy
        softfile_wy = wfilesy[kk]+'_sthr'
        f = open(dirwav+'/'+wfilesy[kk], 'rb')
        ft = open(dirwav+'/'+wfilesTy[kk], 'rb')
        fout=open(dirwav+'/tmp.tmp', 'wb')
        for i in range(dl):
            mybuf=np.fromfile(f, dtype='float32', count=dp)
            mybuft=np.fromfile(ft, dtype='float32', count=dp)
            iineg=mybuf < 0
            datneg = mybuf[mybuf < 0.0]
            if (iineg.size > 0):
                mybuf=abs(mybuf)
                mybuf = mybuf-mybuft
                mybuf[mybuf < 0] = 0
                mybuf[iineg] = - mybuf[iineg]
            fout.write(mybuf)
            
        f.close()
        fout.close()
        ola2filt(dirwav+'/tmp.tmp', dirwav+'/'+softfile_wy, dp, dl, h, h)
    
    inDWT(dirwav, filename, outdir, filename,  nj, dp, dl, 1, doexp)
       
               
                    

from fdwt import writehdr
            

        
def logfile(dir,  filename, outdir, outfile, dp, dl):
    bs=512
    nb = int(dl/bs)
    rem = dl % bs
    f = open(dir+'/'+filename, 'rb')
    fout=open(outdir+'/'+outfile, 'wb')
    for j in range(nb):
        buf=np.fromfile(f, dtype='float32', count = dp*bs)
        buf[buf == 0]=1
        bufexp = np.log(buf)
        #ii = np.isnan(bufexp)
        #bufexp[ii] = 0
        fout.write(bufexp)
    if (rem != 0):
           buf=np.fromfile(f, dtype='float32', count = dp*rem)
           buf[buf == 0] =1
           bufexp = np.log(buf)
           #ii = np.isnan(bufexp)
           #bufexp[ii]=0
           fout.write(bufexp)
    f.close()
    fout.close()
    writehdr(outdir, outfile, dp, dl)
    



                
        
       

        