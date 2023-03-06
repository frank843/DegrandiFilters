# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 18:32:44 2022

@author: Frank De Grandi
"""

import numpy as np
import matplotlib.pyplot as plt
import math

def testfindthr():
    bs=64
    dp = 4192
    dl = 4387
    ymin=192
    xmin=2752
    dir='O:\pythonTest'
    filebck='congoset1_MASTER_MONOSTATIC_HH_pwr_rsp'
    dirwav='O:\pythonTest\wav'
    filename='congo'
    findthr(dir, filebck, dirwav, filename, dp, dl, xmin, ymin)

# given the position xmin, ymin (resolution 64 pixels) of the most homogeneous block
# compute the threholds thrwx, thrwy of the Wx and Wy wavelet coefficients

def findthr(dir, filebck, dirwav, filename, dp, dl, xmin, ymin):
    bs=64
    
    bytenum=4
    f=open(dir+'/'+filebck, 'rb')
# skip ymin lines
    f.seek(dp * ymin * bytenum, 0)

    buf=np.fromfile(f, dtype='float32', count=bs * dp)
    bufr = buf.reshape(bs, dp)
    win = bufr[0:bs, xmin:xmin+bs]
    cv = np.std(win)/np.mean(win)
    print('Bck cv: ', cv)
    f.close()
    ftr=open(dir+'/'+filename+'_trace.txt', 'at')
    print('Bck cv: ', filename, ' ', cv, file=ftr)
    ftr.close()
#dirwav = 'O:\pythonTest\wav'
    nj=4
#filename='congo'

    wfilesx=[filename+'_WX1']
    for j in range(nj-1):
        wfilesx=wfilesx+[filename+'_WX'+str(j+2)]
        print(wfilesx)
    
    wfilesy=[filename+'_WY1']
    for j in range(nj-1):
        wfilesy=wfilesy+[filename+'_WY'+str(j+2)]
        print(wfilesy)

    thrwx = np.zeros(4, dtype='float32')
    thrwy = np.zeros(4, dtype='float32')
    for j in range(nj-1):
        f=open(dirwav+'/'+wfilesx[j], 'rb')
# skip ymin lines
        f.seek(dp * ymin * bytenum, 0)
        buf=np.fromfile(f, dtype='float32', count=bs * dp)
        bufr = buf.reshape(bs, dp)
        win = bufr[0:bs, xmin:xmin+bs]
        print('File: WX', j+1)
        noisevarx1=np.var(win)
        print('Noise variance: ', noisevarx1)
        if (j == 0):
            thrwx1 = 1.5 * math.sqrt(noisevarx1)
        else:
            thrwx1 = math.sqrt(noisevarx1)
            thrwx[j] = thrwx1
            print('Threshold wx1: ', thrwx1)

        #h = np.histogram(win)
        #plt.plot(h[1][0:10], h[0])
        #plt.show
        f.close()

        f=open(dirwav+'/'+wfilesy[j], 'rb')
# skip ymin lines
        f.seek(dp * ymin * bytenum, 0)
        buf=np.fromfile(f, dtype='float32', count=bs * dp)
        bufr = buf.reshape(bs, dp)
        win = bufr[0:bs, xmin:xmin+bs]
        print('File: Wy1')
        noisevary1=np.var(win)
        print('Noise variance: ', noisevary1)
        if (j == 0):
            thrwy1 = 1.5 * math.sqrt(noisevary1)
        else:
            thrwy1 = math.sqrt(noisevary1)
            thrwy[j]=thrwy1
            print('Threshold wy1: ', thrwy1)
        # h = np.histogram(win)
        # plt.plot(h[1][0:10], h[0])
    
        f.close()
        #plt.show()
    return(thrwx, thrwy)






    



