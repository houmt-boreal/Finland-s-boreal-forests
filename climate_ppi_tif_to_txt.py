#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
import csv
import os, glob
from scipy import stats




INPUT_FOLDER= r'G:\mcd43c4_product\ppi_monthly_JJA_10km_col_row_is_finclimate'
files = glob.glob(os.path.join(INPUT_FOLDER, '*08.tif'))

alist=[]
for innc in files:
    raster = gdal.Open(innc)
    data = raster.GetRasterBand(1).ReadAsArray().astype('float')
    data = data.ravel()
    alist.append(data)
cd=np.asarray(alist)
cv=np.transpose(cd)
np.savetxt(r'D:\griddata_fi\new2018\txt\mean_ppi_aug_2002_2018.txt', cv, delimiter=',')
cd=None
cv=None
data=None




