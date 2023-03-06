# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 18:55:51 2022

@author: Frank De Grandi
"""

import numpy as np
from ola2filt import ola2filt
from fdwt import writehdr

def expfile(dir, filename, outdir, outfile, dp, dl):
    bs=512
    nb = int(dl/bs)
    rem = dl % bs
    f = open(dir+'/'+filename, 'rb')
    fout=open(outdir+'/'+outfile, 'wb')
    for j in range(nb):
        buf=np.fromfile(f, dtype='float32', count = dp*bs)
        bufexp = np.exp(buf)
        fout.write(bufexp)
    if (rem != 0):
           buf=np.fromfile(f, dtype='float32', count = dp*rem)
           bufexp = np.exp(buf)
           fout.write(bufexp)
    f.close()
    fout.close()
    writehdr(outdir, outfile, dp, dl)
    

def addfiles(dir, file1, file2, file3, outdir, outfile, norm, dp, dl):
    f1=open(dir+'/'+file1, "rb")
    f2 = open(dir+'/'+file2, "rb")
    f3 = open(dir+'/'+file3, "rb")
    fout=open(outdir+'/'+outfile, 'wb')
    
    for i in range(dl):
        line1=np.fromfile(f1, dtype='float32', count=dp)
        line2=np.fromfile(f2, dtype='float32', count=dp)
        line3=np.fromfile(f3, dtype='float32', count=dp)
        lineout=line1+norm*line2+norm*line3
        fout.write(lineout)
    fout.close
    f1.close
    f2.close
    f3.close
    

def hfilter(level, conjugate):
    if(level == 0):
        fil=np.array([0.0, 0.0, 0.125, 0.375, 0.375, 0.125, 0.0], dtype='float32')
    if (level == 1):
        fil=np.array([0.0, 0.0, 0.125, 0.0, 0.375, 0.0, 0.375, 0.0, 0.125, 0.0, 0.0], dtype='float32')
    if (level == 2):
        fil=np.array([0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.375, 0.0,0.0, 0.0, 0.125, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 3):
        fil=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.375, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 4):
        fil=np.array([0, 0, 0.125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.375, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.375, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.125, 0, 0], dtype='float32')
    if (conjugate == 0): 
        return(fil)
    else: 
        return(np.flipud(fil))        

def kfilter(level, conjugate):
    if (level == 0):
        fil=np.array([0.0078125, 0.054685, 0.171875, -0.171875, -0.054685, -0.0078125, 0.0], dtype='float32')
    if (level == 1 ):
       fil=np.array([0.0  , 0.0078125, 0.0  , 0.0546875, 0.0 , 0.171875, 0.0, -0.171875, 0.0 , -0.0546875, 0.0  , -0.0078125, 0.0], dtype='float32')
    if (level ==2):
        fil=np.array([0.0, 0.0, 0.0  , 0.0078125, 0.0, 0.0, 0.0, 0.0546875, 0.0, 0.0, 0.0 , 0.171875, 0.0, 0.0, 0.0, -0.171875, 0.0, 0.0, 0.0 , -0.0546875, 0.0, 0.0, 0.0,-0.0078125, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 3):
        fil=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0  , 0.0078125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0  , 0.0546875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 , 0.171875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.171875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 , -0.0546875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0078125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype='float32')
    if (conjugate == 0):
        return(fil)
    else:
        return(np.flipud(fil))

def lfilter(level):
    if (level == 0):
        fil=np.array([0.0078125, 0.046875, 0.1171875, 0.65625, 0.1171875, 0.046875, 0.0078125], dtype='float32')
    if (level == 1) :
        fil=np.array([0.0, 0.0078125, 0.0, 0.046875, 0.0,  0.1171875, 0.0, 0.65625, 0.0, 0.1171875, 0.0, 0.046875, 0.0, 0.0078125, 0.0], dtype='float32')
    if (level == 2):
        fil=np.array([0.0, 0.0, 0.0, 0.0078125, 0.0, 0.0, 0.0, 0.046875, 0.0, 0.0, 0.0,0.1171875, 0.0, 0.0, 0.0, 0.65625, 0.0, 0.0, 0.0, 0.1171875, 0.0, 0.0, 0.0, 0.046875, 0.0, 0.0, 0.0, 0.0078125, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 3):
        fil = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0078125, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.046875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1171875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.65625, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1171875,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.046875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0078125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype='float32')
    return(fil)

# inverse dyadic wavelet transform
def inDWT(dir, filename, outdir, outfile,  nj, dp, dl, softh, doexp):
    wfilesx=[filename+'_WX1']
    for j in range(nj-1):
        wfilesx=wfilesx+[filename+'_WX'+str(j+2)]
    print(wfilesx)
    
    wfilesy=[filename+'_WY1']
    for j in range(nj-1):
        wfilesy=wfilesy+[filename+'_WY'+str(j+2)]
    print(wfilesy)
    # if soft thresholding 
    if (softh ==1):
        for j in range(nj-1):
            wfilesx[j]=wfilesx[j]+'_sthr'
        for j in range(nj-1):
            wfilesy[j]=wfilesy[j]+'_sthr'
    lam=[1.5, 1.12, 1.03, 1.01, 1.0]       
    jJ=nj
    # main loop over scales
    for kk in range(nj):
        print('processing scale: ', jJ)
        j = jJ-1
        if (kk == 0):
            fileS=filename+'_S'+str(nj)
        else:
            fileS=filename+'_Stmp'
        norm=lam[j]
        hhole=hfilter(j, 1)
        khole=kfilter(j, 0)
        lhole=lfilter(j)
        ola2filt(dir+'/'+fileS, dir+'/fileS1.tmp', dp, dl, hhole, hhole )
        ola2filt(dir+'/'+wfilesx[j], dir+'/filewx.tmp', dp, dl,  khole, lhole )
        ola2filt(dir+'/'+wfilesy[j], dir+'/filewy.tmp', dp, dl, lhole, khole )
        print(fileS)
        print(wfilesx[j])
        print(wfilesy[j])
        
        if (kk != nj-1):
            addfiles(dir, 'fileS1.tmp', 'filewx.tmp', 'filewy.tmp', dir, filename+'_Stmp', norm, dp, dl)
        else:
            if (doexp == 1):
                addfiles(dir, 'fileS1.tmp', 'filewx.tmp', 'filewy.tmp', outdir, outfile+'_recotmp', 1.0,  dp, dl)
            else:
                addfiles(dir, 'fileS1.tmp', 'filewx.tmp', 'filewy.tmp', outdir, outfile+'_reco', 1.0,  dp, dl)
               
        jJ=jJ-1
    if (doexp == 1):
        expfile(outdir, outfile+'_recotmp', outdir, outfile+'_reco', dp, dl)
    writehdr(outdir, outfile+'_reco', dp, dl)
    print('enf of job')
    

    
            
        