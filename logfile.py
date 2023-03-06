# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:56:22 2022

@author: Frank De Grandi
"""
import numpy as np

def logfile(dir,  filename, outdir, outfile, dp, dl):
    bs=512
    nb = int(dl/bs)
    rem = dl - bs * nb
    print(nb, rem)
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
           
           fout.write(bufexp)
    f.close()
    fout.close()
    writehdr(outdir, outfile, dp, dl)
    
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