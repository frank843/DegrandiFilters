# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 15:35:05 2022

@author: Frank DE Grandi
"""
import numpy as np


def intoTofloat(dir, file, outdir, outfile, dp, dl):
    f=open(dir+'/'+file+'.img', 'rb')
    
    buf = np.fromfile(f, dtype=np.uint16, count=dp*dl)
    buf2=buf.byteswap()
    fout=open(outdir+'/'+outfile, 'wb')
    buf3=buf2.astype('float32')
    fout.write(buf3)
    
    fout.close()
    f.close()
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
    
# sample call
dir='N:/ICEYE/ICEYE_GRD_SM_89766_20210802T055027_Stack'
filelist=['band_1_mst_01Jan2000', 'band_1_slv1_01Jan2000', 'band_1_slv2_01Jan2000', 'band_1_slv3_01Jan2000']
nf=len(filelist)
nf=1
for i in range(nf):
    print(filelist[i])
    intoTofloat(dir, filelist[i], dir, filelist[i]+'_float', 18714, 26641)
    
