# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:15:01 2022

@author: Frank De Grandi
"""
import numpy as np
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
        return(fil[::-1])
    
def gfilter(level, conjugate):
    if(level == 0):
        fil=np.array([0.0, 0.0, 0.0, -2.0, 2.0, 0.0, 0.0], dtype='float32')
    if (level == 1):
        fil=np.array([0.0, 0.0, 0.0, 0.0, -2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 2):
        fil=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -2.0, 0.0, 0.0, 0.0,  2.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0], dtype='float32')
    if (level == 3):
        fil=np.array([.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype='float32')
    if (level == 4):
        
        fil=np.array([0.,  0., -2.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0., 0.,0.,0.,0.,0.,0.,0.,2.0, 0., 0. ], dtype='float32')
    if (conjugate == 0): 
        return(fil)
    else: 
        return(fil[::-1])

# dyadic forward wavelet transform
from ola2filt import ola2filt


# dyadic wavelet transform
def fdwt(dir, infile, outdir, outfile, nj, dp, dl):
    
    sfiles=[outfile+'_S1']
    for j in range(nj-1):
        sfiles=sfiles+[outfile+'_S'+str(j+2)]
    print(sfiles)
    
    wfilesx=[outfile+'_WX1']
    for j in range(nj-1):
        wfilesx=wfilesx+[outfile+'_WX'+str(j+2)]
    print(wfilesx)
    
    wfilesy=[outfile+'_WY1']
    for j in range(nj-1):
        wfilesy=wfilesy+[outfile+'_WY'+str(j+2)]
    print(wfilesy)
    
    for j in range(nj):
        
        hhole=hfilter(j, 0)
        ghole=gfilter(j, 0)
        if (j == 0):
            print('transform step 1')
            ola2filt(dir+'/'+infile, outdir+'/'+outfile+'_S1', dp, dl, hhole, hhole)
            ola2filt(dir+'/'+infile, outdir+'/'+outfile+'_WX1', dp, dl, ghole, hhole)
            ola2filt(dir+'/'+infile, outdir+'/'+outfile+'_WY1', dp, dl, hhole, ghole)
        else:
            print('transform step ', j+1)
            ola2filt(outdir+'/'+sfiles[j-1], outdir+'/'+sfiles[j], dp, dl, hhole, hhole)
            ola2filt(outdir+'/'+sfiles[j-1], outdir+'/'+wfilesx[j], dp, dl, ghole, hhole)
            ola2filt(outdir+'/'+sfiles[j-1], outdir+'/'+wfilesy[j], dp, dl, hhole, ghole)
    writewavhdr(outdir, outfile, dp, dl)
    print('end of job')       
    
def writehdr(dir, filename, dp, dl):
    f=open(dir+'/'+filename+'.hdr', 'wt')
    f.writelines("ENVI\n")
    f.write("samples = "+str(dp)+'\n')
    f.write("lines =   "+str(dl)+"\n")
    f.write("bands =   1\n")
    f.write("headeroffset =   0\n")
    f.write("file type = ENVI Standard\n")
    f.write("data type = 4\n")
    f.write("interleave                = bip")
    f.close()

def writewavhdr(dir, filename, dp, dl):
    writehdr(dir, filename+'_S1', dp, dl)
    writehdr(dir, filename+'_S2', dp, dl)
    writehdr(dir, filename+'_S3', dp, dl)
    writehdr(dir, filename+'_S4', dp, dl)
    
    writehdr(dir, filename+'_WX1', dp, dl)
    writehdr(dir, filename+'_WX2', dp, dl)
    writehdr(dir, filename+'_WX3', dp, dl)
    writehdr(dir, filename+'_WX4', dp, dl)
    
    writehdr(dir, filename+'_WY1', dp, dl)
    writehdr(dir, filename+'_WY2', dp, dl)
    writehdr(dir, filename+'_WY3', dp, dl)
    writehdr(dir, filename+'_WY4', dp, dl)





