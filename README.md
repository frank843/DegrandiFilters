# A suite of time-series and single set InSAR

# coherence and backscatter speckle filters

#### Author:

#### Gianfranco (Frank) De Grandi

#### The filters work in a time-space-scale domain afforded by a wavelet representation. A wavelet s oft-

#### thresholding technique provides, for each dataset, local estimates of the backscatter or the coherence

#### |𝛾𝛾| mean value. Wavelet thresholding is equivalent to local signal averaging with a kernel that adapts to

#### the signal regularity in the neighborhood of each sample. Wavelet thresholds are computed adaptively

#### based on a noise model (speckle or coherence) whose parameters are estimated automatically.

#### Therefore, no processing parameters need to be set by the user.

#### The method is described in detail in chapters 8 and 9 of:

#### De Grandi G. and De Grandi EC., “Spatial Analysis for Radar Remote Sensing of the Tropical Forests”, CRC

#### Press, 2021, ISBN: 978-0- 367 -25940-

#### Related literature:

F. De Grandi, J.S. Lee, M. Simard, and H. Wakabayashi, “ _Speckle filtering, segmentation and classification
of polarimetric SAR data: a unified approach based on the wavelet transform_ ”, _Proceedings, IGARSS
2000_ , Honolulu, HI, USA, paper TU08_05.

F. De Grandi, J.S. Lee, P. Siqueira, A. Baraldi, and M. Simard, “ _Segmentation and labeling of polarimetric
SAR data: Can wavelets help?_ ”, _Proceedings IGARSS 2001_ , Sydney, Australia, paper TU10_01.

S. Mallat, _A Wavelet Tour of Signal Processing_ , 2nd ed., San Diego, CA: Academic Press, pp. 163–219,
1999.

S. Mallat, and S. Zhong, “ _Characterization of signals from multiscale edges_ ”, _IEEE Transactions on
Pattern Analysis and Machine Intelligence_ , vol. 14, no. 7, pp. 710–732, 1992.

D.L. Donoho, “De-noising by soft-thresholding”, _IEEE Transactions on Information Theory_ , vol. 41, no.
3, 613–627, May 1995.

M. Simard, G. De Grandi, K.P.B. Thomson, and G.B. Benie, “Analysis of speckle noise contribution on
wavelet decomposition of SAR images”, _IEEE Transactions on Geoscience and Remote Sensing_ , vol. 36,
no. 6, pp. 1953– 1962

G.F. De Grandi, M. Leysen, J.S. Lee, and D. Schuler, “ _Radar reflectivity estimation using multiple SAR
scenes of the same target: techniques and applications_ ”, _Proceedings IEEE IGARSS'97_ , August 3–8,
1997, Singapore, pp. 1044, November 1998.

R. Touzi, A. Lopez, J. Bruniquel, and P.W. Vachon, “Coherence estimation for SAR imagery”, _IEEE
Transactions on Geoscience and Remote Sensing_ , vol. 37, no. 1, January 1999.

S.R. Cloude, “ _Polarisation, Applications in Remote Sensing_ , Oxford, UK: Oxford University Press, 2010.

R. Touzi, and A. Lopes, “Statistics of the Stokes parameters and of the complex coherence parameters in
one-look and multilook speckle field”, _IEEE Transactions on Geoscience and Remote Sensing_ , vol. 34,
pp. 519–532, March 1996.

J-S. Lee, S.R. Cloude, K.P. Papathanassious, M.R. Grunes, and I.H. Woodhouse, “Speckle filtering and
coherence estimation of polarimetric SAR interferometry data for forest applications”, _IEEE Transactions
on Geoscience and Remote Sensing_ , vol. 41, no. 10, 2254–2263, October 2003.

#### Documentation:

#### Elsa Carla De Grandi


## Input data sets requirements

### Backscatter

#### The filters accept as input ground range detected backscatter intensity data sets (e.g. ENVISAT PRI,

#### Sentinel-1 GRD Level1). Single look sets assure the best performance in terms of spatial resolution.

### Coherence

#### Filtered (e.g. Goldstein) coherence from the flattened interferogram.

## Example installation:
### Create Python Environment
`python3 -m venv .venv`
### Activate Environment
Windows:  
`.venv/Scripts/activate`  
Unix/macOS/Linux:  
`source .venv/bin/activate`  
### Install requirements  
`pip install -r requirements.txt`
### Test installation:
#### Place .tif files inside data folder
### Convert .tif to ENVI
`python3 tifToFloat.py filename.tif`
#### Run Filter
`python3 specklekiller.py filename`
