# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 19:18:30 2022

@author: Frank De Grandi
"""

import numpy as np
from wavsoftdenoise import writehdr

def stripnan(dir, file, outdir, outfile, dp, dl):
    f=open(dir+'/'+file, 'rb')
    fout=open(outdir+'/'+outfile, 'wb')
    for i in range(dl):
        myline=np.fromfile(f, count=dp, dtype='float32')
        ii=np.isnan(myline)
        myline[ii]=0.0
        fout.write(myline)
    f.close()
    fout.close()
    writehdr(outdir, outfile, dp, dl)
    
#sample call
filelist=['set1HH_cc', 'set2HH_cc_rsp', 'set3HH_cc_rsp', 'set4HH_cc_rsp', 'set5HH_cc_rsp', 'set6HH_cc_rsp', 'set6HH_cc_rsp']
for j in range(len(filelist)):
    stripnan('O:/pythonTest/SungaiCC', filelist[j], 'O:/pythonTest/SungaiCC', filelist[j]+'_clean', 3472, 6840)