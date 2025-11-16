# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:28:05 2022

@author: Frank
"""

import numpy as np
import tifffile as tiff

def tifTofloat(dir, tifile, outdir, outfile):
  
  data = tiff.imread(dir+'/'+tifile)
  print("Data type:", data.dtype)
  print('Data shape  ', data.shape)
  
  m = np.mean(data)
  dmax=np.amax(data)
  dmin=np.amin(data)
  print(m, '  ',  dmax, '  ',dmin)
  
  #datafloat=data.astype(np.uint16)
  datafloat=data.astype(np.float32)
  #datafloat=data
  
  """
  fout=open(outdir+'/'+outfile, 'wb')
  fout.write(datafloat)
  fout.close()
  """

  with open(outdir+'/'+outfile, 'wb') as f:
     datafloat.tofile(f)

  print("Out type:", datafloat.dtype)
  print('Out shape  ', datafloat.shape)
  lines, samples=datafloat.shape

  writehdr(outdir, outfile, samples, lines)
  print('sayonara')
  
  
def writehdr(dir, filename, samples, lines):
    f=open(dir+'/'+filename+'.hdr', 'wt')
    f.writelines("ENVI\n")
    f.write("samples = "+str(samples)+'\n')
    f.write("lines = "+str(lines)+"\n")
    f.write("bands = 1\n")
    f.write("headeroffset =   0\n")
    f.write("file type = ENVI Standard\n")
    f.write("data type = 4\n")
    f.write("interleave = bsq")
    f.close()  
  
  
import sys
dir='./data'
tiffile = sys.argv[1] #'ALOS2337193650-200820_WBDR2.2GUD_HH_SLP.tif'
outdir=dir
outfile=tiffile.rsplit('.', 1)[0] #'ALOS2337193650-200820_WBDR2.2GUD_HH_SLP'

tifTofloat(dir, tiffile, outdir, outfile)


