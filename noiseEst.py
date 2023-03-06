# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 17:31:10 2022

@author: Frank De Grandi
"""

# find the position x, y of a stationary area by minimum CV in
# scanning windows 64 x 64

import numpy as np
import matplotlib.pyplot as plt
from fdwt import writehdr

def homoarea(dir, file, dp, dl):
    print('noise estimator')
    bs=64
    nb = int(dl / bs)
    na  = int(dp / bs)
    stat = np.zeros([nb, na], dtype='float32')
    f=open(dir+'/'+file, 'rb')
    #fout=open(dir+'/'+outfile, 'wb')
    mincv=1000.
    xmin=0
    ymin=0
    sdall=np.zeros([nb * na], dtype='float32')
    meanall=np.zeros([nb * na], dtype='float32')
    ii=0
    for j in range(nb):
        buf=np.fromfile(f, dtype='float32', count=dp  * bs)
        
       
        for i in range(dp*bs):
            if (np.isnan(buf[i]) ):
                buf[i] = 0.0
        block= buf.reshape(bs, dp)
        #print(np.mean(block))
        if (j % 10 == 1):
            print(j)
        for k in range(na):
            
            win = block[0:bs, k * bs:k * bs +bs]
            m = np.mean(win)
            sd = np.std(win)
            #print(m)
            if (np.isnan(m)):
                continue
            if (np.isnan(sd)):
                continue
            cv = sd/m
            meanall[ii]=m
            sdall[ii]=sd
            ii=ii+1
            if (np.isnan(cv)):
                continue
            if (cv < mincv):
                mincv= cv
                xmin=k
                ymin=j
    f.close()
    print("minimum cv: ", mincv)
    #print('ENL: ', 1.0 / mincv ** 2)
    print('block pixel position: ', xmin * bs)
    print(' block line position :', ymin * bs)
    ftr=open(dir+'/'+file+'_trace.txt', 'wt')
    print("minimum cv: ", mincv, file=ftr)
    print('ENL: ', 1.0 / mincv ** 2, file=ftr)
    print('block pixel position: ', xmin * bs, file=ftr)
    print(' block line position :', ymin * bs, file=ftr)
    ftr.close()
    jsort=np.argsort(meanall)
    meansort=meanall[jsort]
    sdsort=sdall[jsort]
    #plt.plot(meansort, sdsort)
    #plt.show()
    return(xmin*bs, ymin*bs)
        

             
        
    