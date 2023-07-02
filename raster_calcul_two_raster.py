#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np
# for ext in s:
#     # Get file names
nirmax = "G:/mcd43c4_product/max_nir_fenno20022018.tif"
redmin = "G:/mcd43c4_product/min_red_fenno20022018.tif"
# output = "G:/mcd43c4_product/nir_minus_red20022018.tif"
output = "G:/mcd43c4_product/nir_red_plus_minus_ratio20022018.tif"

# Open band 1 as array
ds = gdal.Open(nirmax)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()

# arr[arr==1e+20] = np.NaN

ds2 = gdal.Open(redmin)
b2 = ds2.GetRasterBand(1)
arr2 = b2.ReadAsArray()
# arr2[arr2==1e+20] = np.NaN

# https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
# https://gis.stackexchange.com/questions/216851/python-script-for-raster-calculation-using-gdal
arr=np.where(((arr <= 1) & (arr >= 0)), arr, np.nan)
arr2=np.where(((arr2 <= 1) & (arr2 >= 0)), arr2, np.nan)
# apply equation
data = arr-arr2
data=(1+data)/(1-data)
# save array, using ds as a prototype
gdal_array.SaveArray(data.astype("float32"), output, "GTIFF", ds)
ds = None
ds2 = None





