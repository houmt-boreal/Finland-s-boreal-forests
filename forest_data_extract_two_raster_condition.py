#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal, gdal_array
import numpy as np

condition = r"E:\ESA_LC\LC_fenno\use_paper\fenno_ESACCI-LC-300m-2013-v2.0.7_epsg4008_mcd43.tif"
output = r"E:\ESA_LC\LC_fenno\use_paper\fenno_ESACCI-LC-300m-2013-v2.0.7_epsg4008_mcd43_50percent.tif"

# Open band 1 as array
ds = gdal.Open(condition)
b1 = ds.GetRasterBand(1)
arr = b1.ReadAsArray()


# data=np.where(((arr < 0) & (arr >= -1)), arr2, np.nan)  # for 50%  0=1-2*50%
# data=np.where(((arr < -0.2) & (arr >= -1)), arr2, np.nan)  # for 60%  -0.2=1-2*60%
data=np.where(((arr < 0) & (arr >= -1)), -1, 1)  # for 55%  -0.05=1-2*52.5%
# apply equation

# data=(1+data)/(1-data)
# save array, using ds as a prototype
gdal_array.SaveArray(data.astype("float32"), output, "GTIFF", ds)
ds = None
# ds2 = None






