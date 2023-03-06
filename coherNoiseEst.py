# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 18:47:09 2022

@author: Frank De Grandi
"""
import numpy as np
import matplotlib.pyplot as plt
from fdwt import fdwt

# NaN in the the cc file must be set to 0

def cohernoiseEst(dir, file, filewav, dirwav, nj, dp, dl):
    nl=64
    nb=int(dl/nl)
    nx=int(dp/nl)
    fileswx=[dirwav+'/'+filewav+'_WX1']
    fileswy=[dirwav+'/'+filewav+'_Wy1']
    for i in range(nj-1):
        fileswx=fileswx+[dirwav+'/'+filewav+'_WX'+str(i+2)]
        fileswy=fileswy+[dirwav+'/'+filewav+'_WY'+str(i+2)]
    
    buf=np.ones([nl, dp], dtype='float32')
    bufw=np.ones([nl, dp], dtype='float32')
    bufw1=np.ones([nj, nl, dp], dtype='float32')
    bufw2=np.ones([nj, nl, dp], dtype='float32')
    meanv=np.ones([nb * nx], dtype='float32')
    sdv=np.ones([nb * nx], dtype='float32')
    varx=np.ones([nj, nb * nx], dtype='float32')
    vary=np.ones([nj, nb * nx], dtype='float32')
    winwx=np.ones([nj, nl, nl], dtype='float32')
    winwy=np.ones([nj, nl, nl], dtype='float32')
    ff=open(dir+'/'+file, 'rb')
    for i in range(nj):
        fwx = [open(i, 'rb') for i in fileswx]
        fwy = [open(i, 'rb') for i in fileswy]
    ii=0
    for i in range(nb):
        bt=np.fromfile(ff, dtype='float32', count=dp*nl)
        buf=bt.reshape(nl, dp)
        for kk in range(nj):
            btw=np.fromfile(fwx[kk], dtype='float32', count=dp*nl)
            bufw1[kk, :, :]=btw.reshape(nl, dp)
            btw=np.fromfile(fwy[kk], dtype='float32', count=dp*nl)
            bufw2[kk, :, :]=btw.reshape(nl, dp)
            #print('block: ', i)
        x=0
        for j in range(nx):
            win=buf[:, x:x+nl]
            mb=np.mean(win)
            vr=np.std(win)
            for kk in range(4):
                winwx[kk, :, :]=bufw1[kk, :, x:x+nl]
                winwy[kk, :, :]=bufw2[kk, :, x:x+nl]
            if (np.count_nonzero(win) < win.size):
                flag=0
            else:
                flag=1
            
            if (np.isfinite(mb) and (flag == 1) and np.isfinite(vr) and  np.all(np.isfinite(winwx))  and np.all( np.isfinite(winwy))):
                meanv[ii]=mb
                sdv[ii]=vr
                for kk in range(4):
                    #wx = winwx[kk, :, :]
                    #wy=winwy[kk, :, :]
                    #wxnz=wx[np.nonzero(wx)]
                    #wynz=wy[np.nonzero(wy)]
                    sdw=np.std(winwx[kk, :, :])
                    varx[kk, ii]=sdw
                    sdw=np.std(winwy[kk, :, :])
                    vary[kk, ii]=sdw
                ii=ii+1
            x = x+nl
    ff.close()
    for f in fwx:
        f.close()
    for f in fwy:
        f.close()
    print('Nr samples: ', ii)
    meanve=meanv[0:ii]
    sdve=sdv[0:ii]
    varxcl=varx[:, 0:ii]
    varycl=vary[:, 0:ii]
    varxsort=np.ones([4, ii], dtype='float32')
    varysort=np.ones([4, ii], dtype='float32')
    jsort=np.argsort(meanve)
    meansort=meanve[jsort]
    sdsort=sdve[jsort]
    for kk in range(nj):
        varxsort[kk, :]=varxcl[kk, jsort]
        varysort[kk, :]=varycl[kk, jsort]
    rwx=np.ones([4, 3], dtype='float32')
    rwy=np.ones([4, 3], dtype='float32')
    
    r=np.polyfit(meansort, sdsort, 2)
    plt.plot(meansort, sdsort)
    plt.show()
    print('Fit coeff: ', r)
    for jj in range(4):
        plt.plot(meansort, varxsort[jj, :])
        plt.show()
        plt.plot(meansort, varysort[jj, :])
        plt.show()
    
    for kk in range(nj):
        xs=varxsort[kk, :]
        ys=varysort[kk, :]
        rx=np.polyfit(meansort,  xs, 2)
        ry = np.polyfit(meansort, ys, 2)
        rwx[kk, :]=rx
        rwy[kk, :]=ry
    plt.plot(meansort, xs)
    plt.plot(meansort, ys)
    plt.show()
    print('WX coeff. ', rwx)
    print('WY coeff. ', rwy)
    return([rwx, rwy])

def wasthrEstimCC(dirwav, file, rwx, rwy, dp, dl):
    nj=4
    fileswx=[dirwav+'/'+file+'_TW1_1']
    fileswy=[dirwav+'/'+file+'_TW2_1']
    for i in range(nj-1):
        fileswx=fileswx+[dirwav+'/'+file+'_TW1_'+str(i+2)]
        fileswy=fileswy+[dirwav+'/'+file+'_TW2_'+str(i+2)]
    filesm = dirwav+'/'+file+'_S3'
    ff=open(filesm, 'rb')
    linein=np.ones(dp, dtype='float32')
    for i in range(nj):
        fwx = [open(i, 'wb') for i in fileswx]
        fwy = [open(i, 'wb') for i in fileswy]
    for kk in range(dl):
        linein=np.fromfile(ff, dtype='float32', count=dp)
        for i in range(nj):
            thrx=rwx[i, 0]+rwx[i, 1] * linein + rwx[i, 2]*np.square(linein)
            thry=rwy[i, 0]+rwy[i, 1] * linein + rwy[i, 2]*np.square(linein)
            fwx[i].write(thrx)
            fwy[i].write(thry)
    ff.close()
    for f in fwx:
        f.close()
    for f in fwy:
        f.close()
    for i in range(nj):
        writehdrfile(fileswx[i], dp, dl )
        

def writehdrfile(filename, dp, dl):
    f=open(filename+'.hdr', 'wt')
    f.writelines("ENVI\n")
    f.write("samples = "+str(dp)+'\n')
    f.write("lines =   "+str(dl)+"\n")
    f.write("bands =   1\n")
    f.write("headeroffset =   0\n")
    f.write("file type = ENVI Standard\n")
    f.write("data type = 4\n")
    f.write("interleave                = bip")
    f.close()

def testwavest(dir, file, dirwav, nl, dp, dl, skipdwt):
    nj=4
    if (skipdwt == 0):
        fdwt(dir, file, dirwav, file, nj, dp, dl)
    rw=cohernoiseEst(dir, file, dirwav, nl, dp, dl)
    rwx=rw[0]
    rwy=rw[1]
    wasthrEstimCC(dirwav, file, rwx, rwy, dp, dl)
        
        
    
        
                    
        
       