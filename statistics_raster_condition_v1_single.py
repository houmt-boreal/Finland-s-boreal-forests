#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np

lc = r"D:\jag_modified\mc43_ppi_finland_10km_rasterio\finland_ESACCI-LC-300m-2002-2018-10km_mode.tif"

# Open band 1 as array
ds = gdal.Open(lc)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()
# arr[arr==1e+20] = np.NaN
np.count_nonzero(arr < 0)   #Counts the number of non-zero values in the array , https://note.nkmk.me/en/python-numpy-count/
# np.count_nonzero(np.isnan(myarray))
# np.count_nonzero(myarray < 3000, axis=0)
np.sum(arr==-1) # 808  # = np.count_nonzero(arr < 0)
data=None
pvalue = r"D:\jag_modified\pls_r2y\ppi_pls_r2y_aug.tif"


ds2 = gdal.Open(pvalue)
b2 = ds2.GetRasterBand(1)
arr2 = b2.ReadAsArray()

data=np.where(((arr == -1) & (arr2 > 0)& (arr2 <= 1)), 999, -9999)
np.sum(data==999)
data=None